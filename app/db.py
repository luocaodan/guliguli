#usr/bin/python
# -*- coding: utf-8 -*-

import time
import threading
import logging
import MySQLdb
import functools
from flask import current_app

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
def runQuerySql(tmplate, parameters, num):
    for k, v in parameters.iteritems():
        parameters[k] = parameters[k].replace("'","\\\'")
        parameters[k] = parameters[k].replace("\"","\\\"")
    sql = tmplate.format(**parameters)
    global _db_ctx
    cursor = None
    current_app.logger.info('SQL: ' + sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        #if transaction
        if num == 1:
            r = cursor.fetchone()
        else:
            r = cursor.fetchall()
        if not r:
            return None
        return r
    finally:
        if cursor:
            cursor.close()

@with_connection
def runInsertSql(tmplate, parameters):
    for k, v in parameters.iteritems():
        parameters[k] = parameters[k].replace("'","\\\'")
        parameters[k] = parameters[k].replace("\"","\\\"")
    sql = tmplate.format(**parameters)
    global _db_ctx
    cursor = None
    current_app.logger.info('SQL: ' + sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        #if transaction
        r = cursor.rowcount
        if _db_ctx.transcations == 0:
            current_app.logger.info('auto commit')
            _db_ctx.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    create_engine('root', '123456buaa', 'guliguli')
