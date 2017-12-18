from flask_mail import Message
from flask import render_template
#from threading import Thread
#import app
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        app.mail.send(msg)

def send_email(to, subject, template, **kw):
    msg = Message('Welcome ' + subject, sender='13987610292@sina.cn', recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    mail.send(msg)
    #thr = Thread(target=send_async_email, args=[app, msg])
    #thr.start()
    #return thr
