# -*- coding: utf-8 -*-
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, jsonify
from . import login_manager
import json
from sqlprocedure import *

class User(UserMixin):
    def __init__(self, userid, username, password, nickname, profile_photo, date_birth, date_register, signature, follow, fans, sex):
        self.id = userid
        self.username = username
        self.password = password
        self.nickname = nickname
        self.profile_photo = profile_photo
        self.date_birth = date_birth
        self.date_register = date_register
        self.signature = signature
        self.follow = follow
        self.fans = fans
        self.sex = sex

    def verifyPassword(self, pwd):
        if pwd == self.password:
            return True
        return False

    def getUserInfo(self):
        c = User(self.id, '', '', self.nickname, self.profile_photo, self.date_birth, self.date_register, self.signature, self.follow , self.fans, self.sex)
        return c

    def getUserParameter(self):
        parameter = {}
        parameter['id'] = self.id
        parameter['pwd'] = self.password
        parameter['nick'] = self.nickname
        parameter['photo'] = self.profile_photo
        parameter['birth'] = self.date_birth
        parameter['reg_date'] = self.date_register
        parameter['signa'] = self.signature
        parameter['fol'] = self.follow
        parameter['fan'] = self.fans
        parameter['sex'] = self.sex
        return parameter

    def updateUserInfo(self, parameter):
        oparameter = self.getUserParameter()
        oparameter.update(parameter)
        template = t_update_user
        #print oparameter
        r = db.runInsertSql(template, oparameter)
        return r
    
    def followUser(self, parameter):
        template = t_insert_follow_user
        r = db.runInsertSql(template, parameter)
        self.updateUserInfo({'fol': self.follow + 1})
        foluser = self.queryByUserid({'id': parameter['uid_2']})
        foluser.updateUserInfo({'fan': foluser.fans + 1})
        return r
    
    def unfollowUser(self, parameter):
        template = t_delete_unfollow_user
        r = db.runInsertSql(template, parameter)
        self.updateUserInfo({'fol': self.follow - 1})
        foluser = self.queryByUserid({'id': parameter['uid_2']})
        foluser.updateUserInfo({'fan': foluser.fans - 1})
        return r

    @staticmethod
    def queryByUsername(parameter):
        template = t_query_user_username
        r = db.runQuerySql(template, parameter, 1)
        if r is None:
            return r
        return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10])

    @staticmethod
    def queryByUserid(parameter):
        template = t_query_user_userid
        r = db.runQuerySql(template, parameter, 1)
        #print r
        if r is None:
            return r
        return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10])

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
    
    @staticmethod
    def hasFollow(parameter):
        template = t_query_relationship
        r = db.runQuerySql(template, parameter, 1)
        if r is None:
            return False
        return True

    @staticmethod
    def getFollows(parameter):
        template = t_query_follows
        r = db.runQuerySql(template, parameter, 2)
        folist = []
        if r is None:
             return folist
        for item in r:
            parameter = {}
            parameter['id'] = item[0]
            parameter['nick'] = item[3]
            parameter['photo'] = item[4]
            parameter['birth'] = item[5]
            parameter['reg_date'] = item[6]
            parameter['signa'] = item[7]
            parameter['fol'] = item[8]
            parameter['fan'] = item[9]
            parameter['sex'] = item[10]
            folist.append(parameter)
        return folist

    @staticmethod
    def getFans(parameter):
        template = t_query_fans
        r = db.runQuerySql(template, parameter, 2)
        fanlist = []
        if r is None:
            return fanlist
        for item in r:
            parameter = {}
            parameter['id'] = item[0]
            parameter['nick'] = item[3]
            parameter['photo'] = item[4]
            parameter['birth'] = item[5]
            parameter['reg_date'] = item[6]
            parameter['signa'] = item[7]
            parameter['fol'] = item[8]
            parameter['fan'] = item[9]
            parameter['sex'] = item[10]
            fanlist.append(parameter)
        return fanlist

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
    def __init__(self, worksid, userid, works_name, content, image, date_post, plateid):
        self.worksid = worksid
        self.userid = userid
        self.works_name = works_name
        self.content = content
        self.image = image
        self.date_post = date_post
        self.plateid = plateid
    
    def getWorksInfo(self):
        p_name = [u'手绘', u'板绘', u'PS', u'厚涂', u'水彩']
        workInfo = {}
        workInfo['w_id'] = self.worksid
        workInfo['u_id'] = self.userid
        workInfo['w_name'] = self.works_name
        workInfo['cont'] = self.content
        try:
            workInfo['img'] =json.loads(self.image)
        except:
            workInfo['img'] = self.image
        workInfo['d_post'] = self.date_post
        workInfo['p_id'] = p_name[self.plateid - 1]
        return workInfo

    @staticmethod
    def queryWorks(parameter):
        tamplate = t_query_works
        p_name = [u'手绘', u'板绘', u'PS', u'厚涂', u'水彩']
        #r = db.query_works(worksid)
        r = db.runQuerySql(tamplate, parameter, 1)
        workInfo = {}
        if r is None:
            return None
        workInfo['w_id'] = r[0]
        workInfo['u_id'] = r[1]
        workInfo['w_name'] = r[2]
        workInfo['cont'] = r[3]
        try:
            workInfo['img'] =json.loads(r[4])
        except:
            workInfo['img'] = r[4]
        workInfo['d_post'] = r[5]
        print r[6]
        workInfo['p_id'] = p_name[r[6] - 1]
        return workInfo
    
    @staticmethod
    def insertWorks(parameter):
        template = t_insert_works
        #r = db.insert_works(u_id, w_name, cont, img, d_post, p_id)
        r = db.runInsertSql(template, parameter)
        template = t_query_lastworks
        r = db.runQuerySql(template, parameter, 1)
        return r[0]
    
    @staticmethod
    def get_nworks(parameter):
        template = t_query_nworks
        l = db.runQuerySql(template, parameter, 2)
        res = []
        if l is None:
            return res
        for r in l:
            w = Works(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            res.append(w.getWorksInfo())
        return res

    @staticmethod
    def get_usersworks(parameter):
        template = t_query_usersworks
        l = db.runQuerySql(template, parameter, 2)
        res = []
        if l is None:
            return res
        for r in l:
            w = Works(r[0], r[1], r[2], r[3], r[4], r[5], r[6])
            res.append(w.getWorksInfo())
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
    def queryComment(parameter):
        template = t_query_comment
        r = db.runQuerySql(template, parameter, 2)
        commentList = []
        if r is None:
            return commentList
        for item in r:
            com = {}
            com['c_id'] = item[0]
            com['txt'] = item[1]
            com['w_id'] = item[2]
            com['u_id'] = item[3]
            com['d_post'] = item[4]
            com['nick'] = item[5]
            com['photo'] = item[6]
            com['sex'] = item[7]
            commentList.append(com)
        return commentList

    @staticmethod
    def insertComment(parameter):
        template = t_insert_comment
        r = db.runInsertSql(template, parameter)
        return r

class Activity():
    def __init__(self, activityid, content, date_release, image):
        self.a_id = activityid
        self.cont = content
        self.d_release = date_release
        self.img = image
    
    @staticmethod
    def hasSignActivity(parameter):
        template = t_query_sign_ac
        r = db.runQuerySql(template, parameter)
        if r[0] == 1:
            return False
        return True

    @staticmethod
    def signActivity(parameter):
        template = t_insert_sign_ac
        r = db.runInsertSql(template, parameter)
        return r

    @staticmethod
    def insertActivity(parameter):
        template = t_insert_activity
        r = db.runInsertSql(template, parameter)
        return r

    @staticmethod
    def signActivity(parameter):
        template = t_delete_sign_ac
        r = db.runInsertSql(template, parameter)
        return r

    @staticmethod
    def query_nActivity(parameter):
        template = t_query_nactivity
        l = db.runQuerySql(template, parameter, 2)
        activityList = []
        if l is None:
            return activityList
        for r in l:
            a = Activity(r[0], r[1], r[2], r[3])
            activityList.append(a)
        return activityList

    @staticmethod
    def queryActivity(parameter):
        template = t_query_activity
        r = db.runQuerySql(template, parameter, 2)
        if r is None:
            return None
        a = Activity(r[0], r[1], r[2], r[3])
        return a
        

class Manager(UserMixin):
    def __init__(self, userid, username, password):
        self.id = userid
        self.name = username
        self.pwd = password
    
    def verifyPassword(self, pwd):
        if pwd == self.pwd:
            return True
        return False

    @staticmethod
    def queryAdmin(parameter):
        template = t_query_admin
        r = db.runQuerySql(template, parameter, 1)
        if r is None:
            return None
        return Manager(r[0], r[1], r[2])
    
    @staticmethod
    def queryAllUser():
        parameter = {}
        template = t_query_alluser
        l = db.runQuerySql(template, parameter, 2)
        userList = []
        if l is None:
            return userList
        for r in l:
            u = User(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10])
            userList.append(u)
        return userList

    @staticmethod
    def deleteUser(parameter):
        template = t_delete_user
        r = db.runInsertSql(template, parameter)
        return r

@login_manager.user_loader
def load_user(userid):
    parameter = {}
    parameter['id'] = userid
    return User.queryByUserid(parameter)