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

'''
@main.route('/rela')
def rela_page():
    return render_template('relationship.html')

@main.route('/')
def home_page():
    topSongsList = mongo.db.sortData.find_one({'tableName' : 'topSongs'})['data']
    data = random.sample(topSongsList, 24)
    return render_template('rcmd.html', data = data) 
        
    
@main.route('/sort/<value>')
def sortSongs_page(value):
    data = mongo.db.sortData.find_one_or_404({'tableName' : value})['data'][0:100]
    if value == 'topComments':
        for comment in data:
            timeStamp = str(comment['time'])[0:10]
            #print timeStamp
            comment['time'] = datetime.datetime.fromtimestamp(int(timeStamp))
    return render_template( value + '.html', data = data)
    
@main.route('/data/<value>')
def data_page(value):
    chartData = mongo.db.chartData.find_one_or_404({'name' : value})['data']
    return render_template( value + '.html', data = chartData)

@main.route('/song/<id>')
def comments_page(id):  
    song_data = mongo.db.sComments.find_one_or_404({'id' : id})
    for comment in song_data['hotComments']:
        timeStamp = str(comment['time'])[0:10]
        #print timeStamp
        comment['time'] = datetime.datetime.fromtimestamp(int(timeStamp)) 
    return render_template('comments.html', data=song_data)
'''