#usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading
import logging
import MySQLdb
import functools
#from models import User

class DBError(Exception):
    pass

#global engine object
engine = None

#ctx
class _LazyConnection(object):
    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            _connection = engine.connect()
            logging.info('[CONNECTION] [OPEN] connection <%s>...' % hex(id(_connection)))
            self.connection = _connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            logging.info('[CONNECTION] [CLOSE] connection <%s>...' % hex(id(_connection)))
            _connection.close()

class _DbCtx(threading.local):
    '''
    sub threads has own local value
    '''
    def __init__(self):
        self.connection = None
        self.transcations = 0
    
    def is_init(self):
        return self.connection is not None

    def init(self):
        logging.info('open lazy connection...')
        self.connection = _LazyConnection()
        self.transcations = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None
    
    def cursor(self):
        return self.connection.cursor()

# thread-local db context:
_db_ctx = _DbCtx()

class _ConnectionCtx(object):
    def __enter__(self):
        """
        获取一个惰性连接对象
        """
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        """
        释放连接
        """
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()

class _Engine(object):
    def __init__(self, connect):
        self._connect = connect  
    
    def connect(self):
        return self._connect()

def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper

def create_engine(user, passwd, db='guliguli', host='127.0.0.1', port=3306, **kw):
    global engine
    if engine is not None:
        raise DBError('Engine is already initailized.')
    params = dict(user=user, passwd=passwd, db=db, host=host, port=port)
    defaults = dict(use_unicode=True) #charset='utf-8') #autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    #params['buffered'] = True
    engine = _Engine(lambda: MySQLdb.connect(**params))
    #test connection...
    logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))

@with_connection
def find_user(username):
    global _db_ctx
    cursor = None
    sql = "call find_user('%s')" % username
    logging.info('SQL: %s' % sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        #if transaction
        if cursor.description:
            names = [x[0] for x in cursor.description]
        r = cursor.fetchone()
        if not r:
            return None
        return r
    finally:
        if cursor:
            cursor.close()

@with_connection
def login_user(username, pwd):
    global _db_ctx
    cursor = None
    sql = "call login_user('%s', '%s')" % (username, pwd)
    logging.info('SQL: %s' % sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        #if transaction
        if cursor.description:
            names = [x[0] for x in cursor.description]
        r = cursor.fetchone()
        if not r:
            return None
        return r
    finally:
        if cursor:
            cursor.close()

@with_connection
def query_by_username(username):
    global _db_ctx
    cursor = None
    sql = "call query_by_username('%s')" % username
    logging.info('SQL: %s' % sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        #if transaction
        if cursor.description:
            names = [x[0] for x in cursor.description]
        r = cursor.fetchone()
        if not r:
            return None
        return r
    finally:
        if cursor:
            cursor.close()

@with_connection
def query_by_userid(userid):
    global _db_ctx
    cursor = None
    sql = "call query_by_userid('%s')" % userid
    logging.info('SQL: %s' % sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        #if transaction
        if cursor.description:
            names = [x[0] for x in cursor.description]
        r = cursor.fetchone()
        if not r:
            return None
        return r
    finally:
        if cursor:
            cursor.close()

@with_connection
def register_user(name, pwd, nick, photo, birth, reg_date, signa, fol, fan):
    global _db_ctx
    cursor = None
    sql = "call register_user('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (name, pwd, nick, photo, birth, reg_date, signa, fol, fan)
    logging.info('SQL: %s' % sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        #if transaction
        r = cursor.rowcount
        if _db_ctx.transcations == 0:
            logging.info('auto commit')
            _db_ctx.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_engine('root', '123456buaa', 'guliguli')
    a = login_user('123456@qq.com', '123456')
    for i in a:
        print i
