from flask import render_template, session, redirect, url_for,flash, current_app, request, jsonify
from datetime import datetime
from . import works
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug import secure_filename
from .. import db
from .. import photos
from ..models import Works, Comment, User
#from ..models import User
from ..email import send_email
import PIL
from PIL import Image
import traceback
import random
import os
import requests

def create_thumbnail(image):
    try:
        base_width = 480
        img = Image.open(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], image))
        print os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], image)
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(current_app.config['THUMBNAIL_FOLDER'], image))

        return True

    except:
        print traceback.format_exc()
        return False

def test_post():
    print 'test_post'
    data = {}
    data['w_name'] = 'Test'
    data['cont'] = str({'text': 'This is a test.', })
    data['img'] =  str(['http://127.0.0.1:5000/_uploads/photos/10.jpg', 'http://127.0.0.1:5000/_uploads/photos/17.jpg'])
    data['d_post'] = '2017-12-12'
    data['p_id'] = '1'

    r = requests.post('http://127.0.0.1:5000/works/post', data=data)
    print r.text

@works.route('/<w_id>')
def worksPage(w_id):
    u_id = current_user.get_id()
    user = None
    if u_id is not None:
        user = User.queryByUserid({'id': u_id}).getUserInfo()
    parameter = {}
    parameter['w_id'] = w_id
    works = Works.queryWorks(parameter)
    if works is not None:
        return render_template('works/works.html', works=works, user=user)
    return render_template("404.html"), 404

@works.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
    u_id = current_user.get_id()
    user = None
    if u_id is not None:
        user = User.queryByUserid({'id': u_id}).getUserInfo()
    if request.method == 'POST':
        parameter = {}
        parameter['u_id'] = current_user.id
        parameter['w_name'] = request.form['w_name']
        parameter['cont'] =request.form['cont']
        parameter['img'] = request.form['img']
        parameter['d_post'] = request.form['d_post']
        parameter['p_id'] = request.form['p_id']
        r = Works.insertWorks(parameter)
        redirect(url_for('works.worksPage', w_id = r))
    return render_template('works/post.html', user=user)

@works.route('/api/uploads', methods = ['GET', 'POST'])
@login_required
def uploads():
    if request.method == 'POST' and 'file' in request.files:
        try:
            files = request.files['file']
            files.filename = secure_filename(files.filename)
            filename = photos.save(files)
            create_thumbnail(filename)
            return jsonify(photos.url(filename))
        except:
            c = []
            return jsonify(c)
    return render_template('works/post.html')

@works.route('/api/postComment', methods = ['GET', 'POST'])
@login_required
def apiPostComment():
    '''
    def test():
        data = {}
        data['txt'] = "This is a test comment"
        data['w_id'] =  '17' #modified this value
        data['d_post'] = '2017-12-12'

        r = requests.post('http://127.0.0.1:5000/works/api/postComment', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['txt'] = request.form['txt']
        parameter['w_id'] = request.form['w_id']
        parameter['u_id'] = '1' #current_user.get_id()
        parameter['d_post'] = request.form['d_post']
        r = Comment.insertComment(parameter)
        if r is None:
            return jsonify(False)
        return jsonify(True)
    return render_template('works/post.html')

@works.route('/api/getComment', methods = ['GET', 'POST'])
@login_required
def apiGetComment():
    '''
    def test():
        data = {}
        data['w_id'] =  '17' #modified this value

        r = requests.post('http://127.0.0.1:5000/works/api/getComment', data=data)
        print r.text
    '''
    if request.method == 'POST':
        parameter = {}
        parameter['w_id'] = request.form['w_id']
        r = Comment.queryComment(parameter)
        if r is None:
            return jsonify([])
        return jsonify(r)
    return render_template('works/post.html')
