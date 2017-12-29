# -*- coding: utf-8 -*-

from flask import render_template, session, redirect, url_for,flash, current_app, request, make_response, jsonify
from datetime import datetime
from . import main
from .forms import NameForm
from flask_login import login_user, login_required, logout_user, current_user
#from .. import db
from ..models import User, Works, Activity
from ..email import send_email
#from .. import mongo
import random
import datetime
from ..models import User


@main.route('/')
@login_required
def home_page():
    curUser = None
    u_id = current_user.get_id()
    if u_id is not None:
        curUser = User.queryByUserid({'id': u_id}).getUserInfo()
    worksList = Works.get_nworks({'n': 6})
    activityList = Activity.query_nActivity({'n': 6})
    return render_template('index.html', user=None, worksList=worksList, activityList=activityList, curUser=curUser)

@main.route('/activity/<a_id>')
@login_required
def activity(a_id):
    user = None
    u_id = current_user.get_id()
    if u_id is not None:
        user = User.queryByUserid({'id': u_id}).getUserInfo()
    parameter = {}
    parameter['a_id'] = a_id
    act = Activity.queryActivity(parameter)
    return render_template('/activity.html', user=user, act=act, curUser=user)

@main.route('/api/insertActivity', methods=['POST', 'GET'])
def insertActivity():
    '''
    def test():
        data = {}
        data['cont'] = u'二次元萌什么~'
        data['d_release'] = '2018-1-1'
        data['img'] = '/static/image/596loyx0vk.png'
        r = requests.post('http://127.0.0.1:5000/api/insertActivity', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['cont'] = request.form['cont']
        parameter['img'] = request.form['img']
        parameter['d_release'] = request.form['d_release']
        r = Activity.insertActivity(parameter)
        return jsonify(r)
    return render_template('index.html')

@main.route('/api/hasSignActivity', methods=['POST', 'GET'])
@login_required
def apiHasSignActivity():
    '''
    def test():
        data = {}
        data['u_id'] = '4'
        data['d_sign'] = '2017-12-12'

        r = requests.post('http://127.0.0.1:5000//api/hasSignActivity', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['u_id'] = current_user.get_id()
        parameter['a_id'] = request.form['a_id']
        parameter['d_sign'] = request.form['d_sign']
        r = Activity.hasSignActivity(parameter)
        return jsonify(r)
    return render_template('index.html')

@main.route('/api/signActivity', methods=['POST', 'GET'])
@login_required
def apiSignActivity():
    '''
    def test():
        data = {}
        data['u_id'] = '4'
        data['d_sign'] = '2017-12-12'

        r = requests.post('http://127.0.0.1:5000//api/signActivity', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['u_id'] = current_user.get_id()
        parameter['a_id'] = request.form['a_id']
        parameter['d_sign'] = request.form['d_sign']
        r = Activity.hasSignActivity(parameter)
        if not r:
            r = Activity.signActivity(parameter)
        return make_response('0', 200)
    return render_template('auth/login.html')