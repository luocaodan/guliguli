from flask import render_template, session, redirect, url_for,flash, current_app, request
from datetime import datetime
from . import works
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug import secure_filename
from .. import db
from .. import photos
from ..models import Works
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
    data['cont'] = {'text': 'This is a test.', 'img': ['http://127.0.0.1:5000/_uploads/photos/10.jpg', 'http://127.0.0.1:5000/_uploads/photos/17.jpg']}
    data['img'] = ''
    data['d_post'] = '2017-12-12'
    data['p_id'] = '1'

    r = requests.post('http://127.0.0.1:5000/works/post', data=data)
    print r.text

@works.route('/<w_id>')
def worksPage(w_id):
    works = Works.queryWorks(w_id)
    if works is not None:
        print works.works_name
        return render_template('works/works.html', works=works, user=current_user)
    return render_template("404.html"), 404

@works.route('/post', methods = ['GET', 'POST'])
#@login_required
def post():
    if request.method == 'POST':
        u_id = 1#current_user.id
        w_name = request.form['w_name']
        cont = request.form['cont']
        img = request.form['img']
        d_post = request.form['d_post']
        p_id = request.form['p_id']
        r = Works.insertWorks(u_id, w_name, cont, img, d_post, p_id)
        print 'insert works: %s' % w_name
        redirect(url_for('works.worksPage', w_id = r))
    return render_template('works/post.html')

@works.route('/api/uploads', methods = ['GET', 'POST'])
@login_required
def uploads():
    if request.method == 'POST' and 'file' in request.files:
        try:
            files = request.files['file']
            files.filename = secure_filename(files.filename)
            filename = photos.save(files)
            create_thumbnail(filename)
            return photos.url(filename)
        except:
            return None
    return render_template('works/post.html')
