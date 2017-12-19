from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm
from app import db
import logging

@auth.route('/login', methods=['POST', 'GET'])
def loginPage():
    return render_template('auth/login.html')

@auth.route('/register', methods=['POST', 'GET'])
def registerPage():
    return render_template('auth/register.html')

@auth.route('/api/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        user = User.queryByUsername(username)
        if user is None:
            return 1
        if user is not None and user.verify_password(pwd):
            login_user(user, True)
            return redirect(request.args.get('next') or url_for('main.home_page'))
            #return 'hello %s'%user.username
        #flash('Invalid username or password.')
        return 2
        #return 'hello %s'%user.username
    return redirect(url_for('auth.loginPage'))

@auth.route('/api/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nickname = request.form['nickname']
        profile_photo = request.form['profile_photo']
        date_birth = request.form['date_birth']
        date_register = request.form['date_register']
        signature = request.form['signature']
        follow = 0
        fans = 0
        r = User.registerUser(username, password, nickname, profile_photo, date_birth, date_register, signature, follow, fans)
        #print r
        #return 'hello %s'%user.username
        #flash('Invalid username or password.')
        #return 0
        return redirect(url_for('auth.login'))
    return redirect(url_for('auth.registerPage'))

@auth.route('/api/login', methods=['POST', 'GET'])
def isHasUser():
    if request.method == 'POST':
        username = request.form['username']
        r = User.find_user(username)
        #flash('Invalid username or password.')
        return r
        #return 'hello %s'%user.username
    return redirect(url_for('auth.loginPage'))

@auth.route('/api/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('main.home_page'))

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