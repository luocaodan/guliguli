from flask import render_template, session, redirect, url_for,flash, current_app
from datetime import datetime
from . import main
from .forms import NameForm
from flask_login import login_user, login_required, logout_user, current_user
#from .. import db
#from ..models import User
from ..email import send_email
#from .. import mongo
import random
import datetime
from ..models import User


@main.route('/')
@login_required
def home_page():
    user = None
    u_id = current_user.get_id()
    if u_id is not None:
        user = User.queryByUserid({'id': u_id}).getUserInfo()
    return render_template('index.html', user=user)
