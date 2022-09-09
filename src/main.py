import tornado.ioloop
import tornado.web
from settings import settings
from utils import set_current_app
from tornado.routing import HostMatches
from models import *
from urls import urls
from settings import SECRET_KEY

def url_wrapper(s: list) -> list:
    wrapper = dict()
    for path, handle, host in s:
        if host not in wrapper:
            wrapper[host] = []
        wrapper[host].append((path, handle))
    
    wrapper_list = []
    for host in wrapper:
        wrapper_list.append((HostMatches(host), wrapper[host]))
    return wrapper_list


application = tornado.web.Application(url_wrapper(urls), **settings, cookie_secret=SECRET_KEY)
set_current_app(application)

create_table()

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()