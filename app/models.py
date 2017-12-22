from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import login_manager


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
        print pwd
        print self.password
        if pwd == self.password:
            return True
        return False
    
    def getFollows(self):
        pass

    @staticmethod
    def queryByUsername(username):
        r =  db.query_by_username(username)
        #print r
        if r is None:
            return r
        return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[6], r[7], r[8], r[9])

    @staticmethod
    def queryByUserid(userid):
        r =  db.query_by_userid(userid)
        #print r
        if r is None:
            return r
        return User(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[6], r[7], r[8], r[9])

    @staticmethod
    def registerUser(name, pwd, nick, photo, birth, reg_date, signa, fol, fan, sex):
        r = db.register_user(name, pwd, nick, photo, birth, reg_date, signa, fol, fan, sex)
        return r

    @staticmethod
    def find_user(name):
        r = db.find_user(name)
        if r[0] == 0:
            return False
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
    def queryWorks(worksid):
        pass
    
    @staticmethod
    def insertWorks(u_id, w_name, cont, img, d_post, p_id):
        pass
    
    @staticmethod
    def get_nworks(n):
        pass

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
    print "log user id = " + userid
    return User.queryByUserid(userid)

'''
class Role(UserMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)


    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''