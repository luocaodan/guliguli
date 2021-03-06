from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from config import config
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

import db

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

IMGCOUNT = 0

#from flask_sqlalchemy import SQLAlchemy
#from flask_pymongo import PyMongo

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
#db = SQLAlchemy()
db.create_engine('root', '123456buaa', 'guliguli')
#mongo = PyMongo()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

photos = UploadSet('photos', IMAGES)
avatar = UploadSet('avatar', IMAGES)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    '''
    app.config.update(
    MONGO_URI='mongodb://localhost:27017/netease',
    MONGO_TEST_URI='mongodb://localhost:27017/test'
    )
    '''
    #app.config['MONGO_DBNAME'] = 'netease'
    
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    #db.init_app(app)
    #mongo.init_app(app)
    login_manager.init_app(app)

    #uploads
    configure_uploads(app, photos)
    configure_uploads(app, avatar)
    patch_request_class(app)

    # attach routes and custom error pages here

    from main import main as main_blueprint
    from auth import auth as auth_blueprint
    from works import works as works_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(works_blueprint, url_prefix='/works')

    return app