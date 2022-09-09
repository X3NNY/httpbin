import json
import io
import uuid
import base64
import pickle
import zipfile
import hashlib
import tornado.web
from models import *
from sqlalchemy import and_, distinct
from sqlalchemy.orm import sessionmaker
from decorator import authenticated
from settings import host, salt
from utils import uploadFile
from utils import downloadFile, downloadFileIO

session_maker = sessionmaker(bind=engine)

def upload(content: bytes, filename=None):
    hash = hashlib.md5(content).hexdigest()
    with session_maker() as session:
        file = session.query(File).filter(File.hash == hash).first()

        if file is not None:
            return file
        
    fname, path, size = uploadFile(content)
    file = File()
    file.filename = fname if filename is None else filename
    file.path = path
    file.hash = hash
    file.size = size
    
    return file


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        try:
            return json.loads(self.get_secure_cookie('user'))
        except Exception:
            return None

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,token")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Content-type", "application/json")
    
    def options(self):
        self.set_status(200)
        self.finish()

class HTMLHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,token")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Max-Age", 1000)

    def get(self):
        return self.render('dist/index.html')

class ReapplyHandler(BaseHandler):
    @authenticated
    def post(self):
        with session_maker() as session:
            randomHost = f'{uuid.uuid4().hex[:6]}.{host}'
            while session.query(session.query(Identifier).filter(Identifier.host == randomHost).exists()).scalar():
                randomHost = f'{uuid.uuid4().hex[:6]}.{host}'
            
            identifier = session.query(Identifier).get(self.current_user['id'])
            identifier.host = randomHost
            session.add(identifier)
            session.commit()
        return self.finish({'code': 200, 'data': None})


class ChangeHandler(BaseHandler):
    @authenticated
    def post(self):
        with session_maker() as session:
            identifier = session.query(Identifier).get(self.current_user['id'])
            if identifier.status == 0:
                identifier.status = 1
            elif identifier.status == 1:
                identifier.status = 0
            
            session.add(identifier)
            session.commit()
            return self.finish({'code': 200, 'data': None})

class LoginHandler(BaseHandler):
    def post(self):
        data = json.loads(self.request.body)
        password = data.get('password', None)
        if not isinstance(password, str):
            return self.finish({'code': 201, 'data': None})
        
        password = hashlib.sha256(password.encode() + salt).hexdigest()

        with session_maker() as session:
            user = session.query(User).filter(User.password == password).first()
            if user is None:
                return self.finish({'code': 201, 'data': None})
            self.set_secure_cookie('user', json.dumps({'uid': user.id, 'id':user.identifier_id}))
            return self.finish({'code': 200, 'data': user.identifier_id})


class RegisterHandler(BaseHandler):
    def post(self):
        data = json.loads(self.request.body)
        password = data.get('password', None)
        if not isinstance(password, str):
            return self.finish({'code': 201, 'data': None})
        
        password = hashlib.sha256(password.encode() + salt).hexdigest()
        with session_maker() as session:
            if session.query(session.query(User).filter(User.password == password).exists()).scalar():
                return self.finish({'code': 202, 'data': None})

            randomHost = f'{uuid.uuid4().hex[:6]}.{host}'
            while session.query(session.query(Identifier).filter(Identifier.host == randomHost).exists()).scalar():
                randomHost = f'{uuid.uuid4().hex[:6]}.{host}'
            identifier = Identifier()
            identifier.host = randomHost
            identifier.status = 1
            session.add(identifier)
            session.commit()

            user = User()
            user.identifier_id = identifier.id
            user.password = password
            session.add(user)
            session.commit()
        return self.finish({'code': 200, 'data': None})


class InfoHandler(BaseHandler):
    @authenticated
    def get(self):
        with session_maker() as session:
            identifier = session.query(Identifier).get(self.current_user['id'])

            return self.finish({'code': 200, 'data': {
                'identifier': identifier.host,
                'status': identifier.status,
                'routes':  identifier.routes,
                'date': identifier.date.timestamp(),
                'total': session.query(HttpLog).filter(HttpLog.identifier_id == identifier.id).count()
            }})


class InfoRoutesHandler(BaseHandler):
    @authenticated
    def get(self):
        with session_maker() as session:
            ret = []
            routes = session.query(Route).filter(Route.identifier_id == self.current_user['id']).all()
            for route in routes:
                ret.append({
                    'id': route.id,
                    'path': route.path,
                })
            return self.finish({'code': 200, 'data': ret})


class RequestListHandler(BaseHandler):
    @authenticated
    def post(self, page: str, size: str):
        page = max(int(page), 1)
        size = max(int(size), 1)
        size = min(size, 20)
        data = json.loads(self.request.body)

        path = data.get('path', '')
        ip = data.get('ip', '')
        ct = data.get('ct', '')
        method = int(data.get('method', 0))

        filters = HttpLog.identifier_id == self.current_user['id']

        if method > 0:
            filters = and_(filters, HttpLog.method == method)
        
        if ct:
            filters = and_(filters, HttpLog.ct == ct)
        
        if ip:
            filters = and_(filters, HttpLog.ip == ip)

        if path:
            filters = and_(filters, HttpLog.path.contains(path, autoescape=True))

        with session_maker() as session:
            httplogs = session.query(HttpLog).order_by(HttpLog.id.desc()).filter(filters).offset((page-1)*size).limit(size)

            ret = []
            for httplog in httplogs:
                ret.append({
                    'id': httplog.id,
                    'path': httplog.path,
                    'method': httplog.method,
                    'ct': httplog.ct,
                    'ua': httplog.ua,
                    'ip': httplog.ip,
                    'date': httplog.date.timestamp()
                })
            
            return self.finish({'code': 200, 'data': {
                'httplogs': ret,
                'total': session.query(HttpLog).filter(filters).count()
            }})


class HttpLogDetailHandler(BaseHandler):
    @authenticated
    def get(self, hid: str):
        hid = int(hid)

        with session_maker() as session:
            httplog = session.query(HttpLog).filter(HttpLog.identifier_id == self.current_user['id'], HttpLog.id == hid).first()
            if httplog is None:
                return self.finish({'code': 201, 'data': None})
            
            raw = downloadFile(httplog.raw.path)
            get = {}
            post = {}
            if httplog.data_id:
                data = pickle.load(downloadFileIO(httplog.data.path))
                get = data.get('GET', {})
                post = data.get('POST', {})

                if httplog.ct.startswith('multipart/form-data') or httplog.ct == 'application/octet-stream':
                    for key in post:
                        if isinstance(post[key], list):
                            tmp = []
                            for fid in post[key]:
                                file = session.query(File).get(post[key])
                                tmp.append((file.hash, file.filename, file.size))
                            post[key] = tmp
            
            return self.finish({'code': 200, 'data': {
                'raw': base64.b64encode(raw).decode(),
                'get': get,
                'post': post
            }})


class SearchCTHandler(BaseHandler):
    @authenticated
    def post(self):
        data = json.loads(self.request.body)
        ct = data.get('ct', '')

        with session_maker() as session:
            res = session.query(distinct(HttpLog.ct)).filter(HttpLog.identifier_id == self.current_user['id'], HttpLog.ct.startswith(ct)).all()
            ret = [row[0] for row in res]
            return self.finish({'code': 200, 'data': ret}) 


class SearchIPHandler(BaseHandler):
    @authenticated
    def post(self):
        data = json.loads(self.request.body)
        ip = data.get('ip', '')

        with session_maker() as session:
            res = session.query(distinct(HttpLog.ip)).filter(HttpLog.identifier_id == self.current_user['id'], HttpLog.ip.startswith(ip)).all()
            ret = [row[0] for row in res]
            return self.finish({'code': 200, 'data': ret}) 


class DownloadHandler(BaseHandler):
    @authenticated
    def post(self):
        data = json.loads(self.request.body)
        ids = data.get('ids')

        if not isinstance(ids, list):
            return 201, None

        with session_maker() as session:
            httplogs = session.query(HttpLog).filter(HttpLog.id.in_(ids), HttpLog.identifier_id == self.current_user['id']).all()

            zfio = io.BytesIO()
            with zipfile.ZipFile(zfio, 'w', zipfile.ZIP_DEFLATED) as zf:
                for httplog in httplogs:
                    zf.writestr(f'{httplog.id}.log', downloadFile(httplog.raw.path))
            
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment;filename=Achieve.zip')

        self.write(zfio.getvalue())
        self.finish()


class DownloadAllHandler(BaseHandler):
    @authenticated
    def post(self):
        with session_maker() as session:
            httplogs = session.query(HttpLog).filter(HttpLog.identifier_id == self.current_user['id']).all()

            zfio = io.BytesIO()
            with zipfile.ZipFile(zfio, 'w', zipfile.ZIP_DEFLATED) as zf:
                for httplog in httplogs:
                    zf.writestr(f'{httplog.id}.log', downloadFile(httplog.raw.path))
            
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment;filename=Achieve.zip')

        self.write(zfio.getvalue())
        self.finish()


class DeleteHandler(BaseHandler):
    @authenticated
    def post(self):
        data = json.loads(self.request.body)
        ids = data.get('ids')

        if not isinstance(ids, list):
            return 201, None

        with session_maker() as session:
            session.query(HttpLog).filter(HttpLog.id.in_(ids), HttpLog.identifier_id == self.current_user['id']).delete()
            session.commit()

class DeleteAllHandler(BaseHandler):
    @authenticated
    def post(self):
        with session_maker() as session:
            session.query(HttpLog).filter(HttpLog.identifier_id == self.current_user['id']).delete()
            session.commit()


class RouteAddHandler(BaseHandler):
    @authenticated
    def post(self):
        response = self.request.body_arguments.get('response', [''])[0].decode()
        path = self.request.body_arguments.get('path', [''])[0].decode()
        file = self.request.files.get('file', [None])[0]

        if not path.startswith('/'):
            return self.finish({'code': 201, 'data': None})

        with session_maker() as session:
            if session.query(session.query(Route).filter(Route.path == path, Route.identifier_id == self.current_user['id']).exists()).scalar():
                return self.finish({'code': 202, 'data': None})
            if file is None:
                response = upload(response.encode())
            else:
                response = upload(file.body)

            session.add(response)
            session.commit()

            route = Route()
            route.identifier_id = self.current_user['id']
            route.path = path
            route.response_id = response.id
            session.add(route)
            session.commit()
            return self.finish({'code': 200, 'data': route.id})


class RouteHandler(BaseHandler):
    @authenticated
    def get(self, rid: str):
        rid = int(rid)
        with session_maker() as session:
            route = session.query(Route).filter(Route.id == rid, Route.identifier_id == self.current_user['id']).first()
            if route is None:
                return self.finish({'code': 201, 'data': None})
            
            response = downloadFile(route.response.path)

            return self.finish({'code': 200, 'data': {
                'id': route.id,
                'path': route.path,
                'response': base64.b64encode(response).decode()
            }})
    
    @authenticated
    def post(self, rid: str):
        response = self.request.body_arguments.get('response', [''])[0].decode()
        path = self.request.body_arguments.get('path', [''])[0].decode()
        file = self.request.files.get('file', [None])[0]
        rid = int(rid)
        with session_maker() as session:
            route = session.query(Route).filter(Route.id == rid, Route.identifier_id == self.current_user['id']).first()
            if route is None:
                return self.finish({'code': 201, 'data': None})
            
            response = upload(response.encode())
            session.add(response)
            session.commit()

            route.response_id = response.id
            session.add(route)
            session.commit()
        return self.finish({'code': 200, 'data': None})
    
    @authenticated
    def delete(self, rid: str):
        rid = int(rid)
        with session_maker() as session:
            session.query(Route).filter(Route.id == rid, Route.identifier_id == self.current_user['id']).delete()
            session.commit()
        return self.finish({'code': 200, 'data': None})


class FileDownloadHandler(BaseHandler):
    @authenticated
    def post(self, hash: str):
        with session_maker() as session:
            file = session.query(File).filter(File.hash == hash).first()

            if file is None:
                return self.finish({'code': 201, 'data': None})

            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', f'attachment;filename={file.filename}')

            self.write(downloadFile(file.path))
            return self.finish()
            

class ReceiveHandler(tornado.web.RequestHandler):
    def procedure(self):
        req_host = self.request.host.strip()[:-len(host)-1]
        suffix = req_host.split('.')[-1]

        ua = self.request.headers.get('User-Agent', '')
        ct = self.request.headers.get('Content-Type', '')

        # www. FAKE RAW CONTENT
        raw = f'''{self.request.method} {self.request.uri} {self.request.protocol}
{self.request.headers}
'''.replace('\n', '\r\n').encode() + self.request.body

        raw = upload(raw)

        get_content = self.request.query_arguments.copy()
        post_content = self.request.body_arguments.copy()

        get_content = {x: get_content.get(x)[0].decode() for x in get_content}
        post_content = {x: post_content.get(x)[0].decode() for x in post_content}

        if ct == 'application/json':
            post_content.update(json.loads(self.request.body))

        for name in self.request.files:
            post_content[name] = []
            for file in self.request.files[name]:
                file = upload(file.body, file.filename)
                post_content[name].append(file)

        with session_maker() as session:
            identifier = session.query(Identifier).filter(Identifier.host == f'{suffix}.{host}').first()
            if identifier is None or identifier.status != 1:
                return

            httplog = HttpLog()
            httplog.identifier_id = identifier.id
            httplog.ct = ct
            httplog.ua = ua
            httplog.method = ['', 'GET', 'POST', 'OPTIONS', 'HEAD', 'PUT', 'DELETE', 'PATCH'].index(self.request.method)
            httplog.ip = self.request.remote_ip
            httplog.path = self.request.path

            session.add(raw)

            for name in self.request.files:
                for file in post_content[name]:
                    session.add(file)
            
            session.commit()

            for name in self.request.files:
                post_content[name] = [file.id for file in post_content[name]]
            
            if get_content or post_content:
                data = pickle.dumps({
                    'GET': get_content,
                    'POST': post_content,
                })
                dataFile = upload(data)
                session.add(dataFile)
                session.commit()
                
                httplog.data_id = dataFile.id

            httplog.raw_id = raw.id
            session.add(httplog)
            session.commit()

            route = session.query(Route).filter(Route.identifier_id == identifier.id, Route.path == self.request.path).first()
            if route is not None:
                response = downloadFile(route.response.path)
                return self.finish(response)

            return self.finish({'code': 200, 'data': None})
            

    def get(self):
        self.procedure()
    
    def post(self):
        self.procedure()
    
    def options(self):
        self.procedure()
    
    def head(self):
        self.procedure()
    
    def delete(self):
        self.procedure()
    
    def put(self):
        self.procedure()
    
    def patch(self):
        self.procedure()
