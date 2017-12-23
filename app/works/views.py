from flask import render_template, session, redirect, url_for,flash, current_app, request
from datetime import datetime
from . import works
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug import secure_filename
from .. import db
from .. import photos
#from ..models import User
from ..email import send_email
import PIL
from PIL import Image
import traceback
import random
import os

def gen_file_name(filename):
    '''
    If file exits, then gen a new filename
    '''
    i = 1

    while os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1
    
    return filename

def create_thumbnail(image):
    try:
        base_width = 80
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

@works.route('/')
def worksPage():
    return render_template('works/post.html')

@works.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        if 'file' in request.files:
            filename = photos.save(request.files['file'])
            create_thumbnail(filename)
            return photos.url(filename)
    return render_template('works/post.html')
