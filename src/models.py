from email.policy import default
import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, Float, Text, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

base = declarative_base()
engine = create_engine('sqlite:///anna.db')

class Identifier(base):
    __tablename__ = 'identifier'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String(128), nullable=False)
    
    status = Column(Integer, default=0)
    '''
        0 -> close
        1 -> open
        2 -> delete
    '''

    # 路由数
    routes = Column(Integer, default=0)
    # 创建时间
    date = Column(DateTime, nullable=False, default=datetime.utcnow)


class HttpLog(base):
    __tablename__ = 'httplog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier_id = Column(Integer, ForeignKey('identifier.id'))
    identifier = relationship('Identifier', backref='HttpLogSet')
    
    # 请求方法
    method = Column(Integer)
    '''
        1 -> GET
        2 -> POST
        3 -> OPTIONS
        4 -> HEAD
        5 -> PUT
        6 -> DELETE
        7 -> PATCH
    '''

    # 请求IP
    ip = Column(String(16))
    
    # Content-Type
    ct = Column(String(64), default='')

    # 请求路径
    path = Column(String(64))
    

    # User-Agent
    ua = Column(String(256), default='')

    # 请求时间
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

    raw_id = Column(Integer, ForeignKey('file.id'))
    raw = relationship('File', foreign_keys=[raw_id])

    data_id = Column(Integer, ForeignKey('file.id'))
    data = relationship('File', foreign_keys=[data_id])


class Route(base):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier_id = Column(Integer, ForeignKey('identifier.id'))
    identifier = relationship('Identifier', backref='RouteSet')

    path = Column(String(32))

    response_id = Column(Integer, ForeignKey('file.id'))
    response = relationship('File')


class File(base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(128))
    filename = Column(String(64))
    hash = Column(String(32))

    # 文件大小（B）
    size = Column(Integer)


class User(base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    identifier_id = Column(Integer, ForeignKey('identifier.id'))
    identifier = relationship('Identifier', backref='User')

    password = Column(String(64))


def create_table():
    base.metadata.create_all(engine, checkfirst=True)