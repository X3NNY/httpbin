from datetime import datetime
import json
import os
from typing import IO, Optional
import uuid
from tornado.web import Application

from settings import BASE_DIR

_GLOBAL = {}


def set_current_app(app: Application) -> None:
    global _GLOBAL
    _GLOBAL['app'] = app


def get_current_app() -> Optional[Application]:
    global _GLOBAL
    return _GLOBAL.get('app', None)


def set_setting(key: str, value: any) -> None:
    """
    设置配置项
    """
    global _GLOBAL
    _GLOBAL[key] = value


def get_setting(key: str) -> Optional[any]:
    """
    获取配置项
    """
    global _GLOBAL
    return _GLOBAL.get(key, None)


def downloadFile(path: str) -> bytes:
    """
    读取文件内容
    """
    path = os.path.join(BASE_DIR, 'files', path)
    with open(path, 'rb') as f:
        return f.read()


def downloadFileIO(path: str) -> IO:
    path = os.path.join(BASE_DIR, 'files', path)
    return open(path, 'rb')


def uploadFile(content: bytes) -> str:
    """
    写入文件内容
    """
    date = datetime.utcnow()
    filename = f'{uuid.uuid4().hex}.bin'
    fpath = os.path.join(str(date.year), str(date.month), str(date.day))
    path = os.path.join(BASE_DIR, 'files', fpath)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(os.path.join(path, filename), 'wb+') as f:
        f.write(content)
    
    return filename, os.path.join(path, filename), os.path.getsize(path)
