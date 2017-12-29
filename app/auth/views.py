# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, make_response, current_app, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User, Manager, Works
from ..email import send_email
from .forms import LoginForm, RegistrationForm
from app import db
import logging
import PIL
from PIL import Image
import traceback
import os
from .. import avatar
from werkzeug import secure_filename

def create_avatar(image):
    try:
        base_width = 140
        img = Image.open(os.path.join(current_app.config['UPLOADED_AVATAR_DEST'], image))
        w = img.size[0]
        h = img.size[1]
        if w > h:
            x = int(float(w - h)/2)
            img = img.crop((x, 0, x + h, h))
        if w < h:
            y = int(float(h - w)/2)
            img = img.crop((0, y, w, y + w))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(current_app.config['UPLOADED_AVATAR_DEST'], image))

        return True

    except:
        print traceback.format_exc()
        return False

@auth.route('/login', methods=['POST', 'GET'])
def login():
    #form = LoginForm()
    if request.method == 'POST':
        return redirect(request.args.get('next') or url_for('main.home_page'))
    return render_template('auth/login.html')

@auth.route('/adminLogin', methods=['POST', 'GET'])
def adminLogin():
    #form = LoginForm()
    if request.method == 'POST':
        parameter = {}
        parameter['name'] = request.form['username']
        parameter['pwd'] = request.form['password']
        admin = Manager.queryAdmin(parameter)
        if admin is None:
            return make_response('1', 200)
        if admin is not None and admin.verifyPassword(parameter['pwd']):
            login_user(admin, True)
            userList = admin.queryAllUser()
            current_app.logger.info('login user %s' % parameter['name'])
            return render_template('auth/manager.html', userList=userList)
        resp = make_response('2', 200)
        return resp
    return render_template('auth/adminLogin.html')

@auth.route('/userinfo', methods=['POST', 'GET'])
@login_required
def userinfo():
    #form = LoginForm()
    u_id = current_user.get_id()
    user = None
    if u_id is not None:
        user = User.queryByUserid({'id': u_id}).getUserInfo()
    return render_template('auth/userinfo.html', user=user)

@auth.route('/api/login', methods=['POST', 'GET'])
def apiLogin():
    if request.method == 'POST':
        parameter = {}
        parameter['name'] = request.form['username']
        parameter['pwd'] = request.form['password']
        user = User.queryByUsername(parameter)
        if user is None:
            return make_response('1', 200)
        if user is not None and user.verifyPassword(parameter['pwd']):
            login_user(user, True)
            current_app.logger.info('login user %s' % parameter['name'])
            return make_response('0', 200)
        resp = make_response('2', 200)
        return resp
    return render_template('auth/login.html')

@auth.route('/api/adminLogin', methods=['POST', 'GET'])
def apiadminLogin():
    if request.method == 'POST':
        parameter = {}
        parameter['name'] = request.form['username']
        parameter['pwd'] = request.form['password']
        admin = Manager.queryAdmin(parameter)
        if admin is None:
            return make_response('1', 200)
        if admin is not None and admin.verifyPassword(parameter['pwd']):
            login_user(admin, True)
            current_app.logger.info('login user %s' % parameter['name'])
            return make_response('0', 200)
        resp = make_response('2', 200)
        return resp
    return render_template('auth/adminLogin.html')

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        parameter = {}
        parameter['name'] = request.form['username']
        parameter['pwd'] = request.form['password']
        parameter['nick'] = request.form['nickname']
        parameter['photo'] = url_for('static', filename = 'image/no_photo.png')
        parameter['birth'] = request.form['date_birth']
        parameter['reg_date'] = request.form['date_register']
        parameter['signa'] = request.form['signature']
        parameter['sex'] = request.form['sex']
        parameter['fol'] = '0'
        parameter['fan'] = '0'
        if User.queryByUsername(parameter) is not None:
            resp = make_response('1', 200)
            return resp
        r = User.registerUser(parameter)
        current_app.logger.info('register user %s' % parameter['name'])
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/api/isHasUser', methods=['POST', 'GET'])
def isHasUser():
    if request.method == 'POST':
        parameter = {}
        parameter['name'] = request.form['username']
        r = User.find_user(parameter)
        if r > 0:
            resp = make_response('1', 200)
            return resp
        else:
            resp = make_response('0', 200)
            return resp
        #return 'hello %s'%user.username
    return redirect(url_for('auth.loginPage'))

@auth.route('/api/logout')
@login_required
def logout():
    logout_user()
    current_app.logger.info('logout user')
    return redirect(url_for('main.home_page'))

@auth.route('/space/<u_id>')
@login_required
def space(u_id):
    user = User.queryByUserid({'id': u_id})
    if user is None:
        return render_template("404.html"), 404
    user = user.getUserInfo()
    if current_user.get_id() is not None and int(user.id) == int(current_user.get_id()):
        user.own = True
    else:
        user.own = False
    worksList = Works.get_usersworks({'u_id': u_id})
    return render_template('auth/space.html', user=user, worksList=worksList)

@auth.route('/api/hasFollow', methods=['POST', 'GET'])
@login_required
def apiHasFollow():
    '''
    def test():
        data = {}
        data['uid_2'] = '4'

        r = requests.post('http://127.0.0.1:5000/auth/api/follow', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['uid_1'] = current_user.get_id()
        parameter['uid_2'] = request.form['uid_2']
        user_1 = User.queryByUserid({'id': parameter['uid_1']})
        r = user_1.hasFollow(parameter)
        return jsonify(r)
    return render_template('auth/login.html')

@auth.route('/api/follow', methods=['POST', 'GET'])
@login_required
def apiFollow():
    '''
    def test():
        data = {}
        data['uid_2'] = '4'
        data['d_follow'] = '2017-12-12'

        r = requests.post('http://127.0.0.1:5000/auth/api/follow', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['uid_1'] = current_user.get_id()
        parameter['uid_2'] = request.form['uid_2']
        parameter['d_follow'] = request.form['d_follow']
        user_1 = User.queryByUserid({'id': parameter['uid_1']})
        r = user_1.hasFollow(parameter)
        if not r:
            r = user_1.followUser(parameter)
        current_app.logger.info('follow user %s' % parameter['uid_2'])
        return make_response('0', 200)
    return render_template('auth/login.html')

@auth.route('/api/unfollow', methods=['POST', 'GET'])
@login_required
def apiUnfollow():
    '''
    def test():
        data = {}
        data['uid_2'] = '4'
        data['d_follow'] = '2017-12-12'

        r = requests.post('http://127.0.0.1:5000/auth/api/unfollow', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['uid_1'] = current_user.get_id()
        parameter['uid_2'] = request.form['uid_2']
        parameter['d_follow'] = request.form['d_follow']
        user_1 = User.queryByUserid({'id': parameter['uid_1']})
        r = user_1.hasFollow(parameter)
        if r is None:
            return make_response('1', 200)
        user_1.unfollowUser(parameter)
        current_app.logger.info('unfollow user %s' % parameter['uid_2'])
        return make_response('0', 200)
    return render_template('auth/login.html')

@auth.route('/api/getFollows', methods=['POST', 'GET'])
@login_required
def apiGetFollows():
    '''
    def test():
        data = {}
        data['uid_2'] = '1'
        data['d_follow'] = '2017-12-12'

        r = requests.post('http://127.0.0.1:5000/auth/api/getFollows', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['id'] = current_user.get_id()
        follows = User.getFollows(parameter)
        return jsonify(follows)
    return render_template('auth/login.html')

@auth.route('/api/getFans', methods=['POST', 'GET'])
@login_required
def apiGetFans():
    '''
    def test():
        data = {}
        data['uid_2'] = '4'
        data['d_follow'] = '2017-12-12'
        
        r = requests.post('http://127.0.0.1:5000/auth/api/getFans', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['id'] = current_user.get_id()
        follows = User.getFans(parameter)
        return jsonify(follows)
    return render_template('auth/login.html')

@auth.route('/api/updateInfo', methods=['POST', 'GET'])
@login_required
def apiUpdateInfo():
    '''
    def test():
        data = {}
        data['nick'] = 'update user'
        data['photo'] = '/static/image/no_photo.png'
        data['signa'] = 'this is update info test'
        data['sex'] = 'this is update info test'
        r = requests.post('http://127.0.0.1:5000/auth/api/updateInfo', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['id'] = current_user.get_id()
        parameter['nick'] = request.form['nick']
        parameter['photo'] = request.form['photo']
        parameter['signa'] = request.form['signa']
        parameter['sex'] = request.form['sex']
        user = User.queryByUserid({'id': parameter['id']})
        r = user.updateUserInfo(parameter)
        return jsonify(True)
        #return jsonify(False)
    return render_template('auth/login.html')

@auth.route('/api/deleteUser', methods=['POST', 'GET'])
def apiDeleteUser():
    if request.method == 'POST':
        parameter = {}
        parameter['id'] = request.form['id']
        r = Manager.deleteUser(parameter)
        if r:
            return jsonify(True)
        return jsonify(False)
        #return jsonify(False)
    return render_template('auth/login.html')

@auth.route('/api/uploads', methods = ['GET', 'POST'])
@login_required
def uploads():
    if request.method == 'POST' and 'file' in request.files:
        try:
            files = request.files['file']
            files.filename = secure_filename(files.filename)
            filename = avatar.save(files)
            create_avatar(filename)
            return jsonify(avatar.url(filename))
        except:
            c = []
            return jsonify(c)
    return render_template('works/post.html')

'''
@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html', user=current_user)

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your account', 'mail/confirm', token=token, user=current_user.username)
    flash('A new confirmation email has been sent to you by email!')
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
            #return 'hello %s'%user.username
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expried!')
    return redirect(url_for('main.index'))
'''