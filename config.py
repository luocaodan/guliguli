import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TREARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky admin <malxi@null.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '@qq.com'
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, '/static/uploads/')
    THUMBNAIL_FOLDER = os.path.join(basedir, '/static/uploads/thumbnail/')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    HOST = '0.0.0.0'
    PORT = 80
    
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    #MONGO_USERNAME='bjhee',
    #MONGO_PASSWORD='111111',
    MONGO_DBNAME = 'netease'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.sina.cn'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '@sina.cn'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '@'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASR_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {'development': DevelopmentConfig, 'testing': TestingConfig, 'production': ProductionConfig, 'default': DevelopmentConfig}
