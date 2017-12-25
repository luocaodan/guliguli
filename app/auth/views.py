# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, make_response, current_app, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm
from app import db
import logging


@auth.route('/login', methods=['POST', 'GET'])
def login():
    #form = LoginForm()
    if request.method == 'POST':
        return redirect(request.args.get('next') or url_for('main.home_page'))
    return render_template('auth/login.html')

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
    user = User.queryByUserid({'id': u_id}).getUserInfo()
    if user.id == current_user.get_id():
        user.own = True
    else:
        user.own = False
    return render_template('auth/space.html', user=user)

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
        if not r:
            return jsonify(False)
        return jsonify(True)
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
        r = requests.post('http://127.0.0.1:5000/auth/api/updateInfo', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['id'] = current_user.get_id()
        parameter['nick'] = request.form['nick']
        parameter['photo'] = request.form['photo']
        parameter['signa'] = request.form['signa']
        user = User.queryByUserid({'id': parameter['id']})
        r = user.updateUserInfo(parameter)
        if r:
            return jsonify(True)
        return jsonify(False)
    return render_template('auth/login.html')

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