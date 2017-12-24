from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import login_manager
import json
from sqlprocedure import *

class User(UserMixin):
    def __init__(self, userid, username, password, nickname, profile_photo, date_brith, date_register, signature, follow, fans, sex):
        self.id = userid
        self.username = username
        self.password = password
        self.nickname = nickname
        self.profile_photo = profile_photo
        self.date_brith = date_brith
        self.date_register = date_register
        self.signature = signature
        self.follow = follow
        self.fans = fans
        self.sex = sex

    def verifyPassword(self, pwd):
        if pwd == self.password:
            self.password = ''
            return True
        return False
    
    def getFollows(self):
        pass

    def getUserInfo(self):
        return User(self.id, '', '', self.nickname, self.profile_photo, self.date_brith, self.date_register, self.signature, self.follow , self.fans, self.sex)

    @staticmethod
    def queryByUsername(parameter):
        template = t_query_user_username
        r = db.runQuerySql(template, parameter, 1)
        if r is None:
            return r
        return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[6], r[7], r[8], r[9])

    @staticmethod
    def queryByUserid(parameter):
        template = t_query_user_userid
        r = db.runQuerySql(template, parameter, 1)
        #print r
        if r is None:
            return r
        return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[6], r[7], r[8], r[9])

    @staticmethod
    def registerUser(parameter):
        template = t_insert_user
        r = db.runInsertSql(template, parameter)
        return r

    @staticmethod
    def find_user(parameter):
        template = t_query_countuser_username
        r = db.runQuerySql(template, parameter, 1)
        if r[0] == 0:
            return False
        return True

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        return True

class Works():
    def __init__(self, worksid, userid, works_name, content, image, date_post, palteid):
        self.worksid = worksid
        self.userid = userid
        self.works_name = works_name
        self.content = content
        self.image = image
        self.date_post = date_post
        self.palteid = palteid
    
    @staticmethod
    def queryWorks(parameter):
        tamplate = t_query_works
        #r = db.query_works(worksid)
        r = db.runQuerySql(tamplate, parameter, 1)
        if r is None:
            return None
        return Works(r[0], r[1], r[2], r[3] , r[4], r[5], r[6])
    
    @staticmethod
    def insertWorks(parameter):
        tamplate = t_insert_works
        #r = db.insert_works(u_id, w_name, cont, img, d_post, p_id)
        r = db.runInsertSql(tamplate, parameter)
        return r
    
    @staticmethod
    def get_nworks(n):
        res = []
        cur = db.get_nworks(n)
        for r in cur:
            res.append(Works(r[0], r[1], r[2], r[3], r[4], r[5], r[7]))
        return res

class Plate():
    def __init__(self, plateid, introduction):
        self.plateid = plateid
        self.introduction = introduction
    
    def get_nworks(self, n):
        pass
    
    @staticmethod
    def queryPlate(palteid):
        pass

class Comment():
    def __init__(self, commentid, text, worksid, userid, date_post):
        self.commentid = commentid
        self.text = text
        self.worksid = worksid
        self.userid = userid
        self.date_post = date_post
    
    @staticmethod
    def queryComment(commentid):
        pass

class Activity():
    def __init__(self, activityid, content, date_release):
        self.activityid = activityid
        self.content = content
        self.date_release = date_release
    
    def signActivity(self):
        pass

    @staticmethod
    def queryActivity(commentid):
        pass


@login_manager.user_loader
def load_user(userid):
    parameter = {}
    parameter['id'] = userid
    return User.queryByUserid(parameter)