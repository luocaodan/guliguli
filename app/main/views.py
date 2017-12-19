from flask import render_template, session, redirect, url_for,flash, current_app
from datetime import datetime
from . import main
from .forms import NameForm
#from .. import db
#from ..models import User
from ..email import send_email
#from .. import mongo
import random
import datetime


@main.route('/')
def home_page():
    return render_template('index.html')
