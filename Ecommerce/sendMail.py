from flask import Flask
from flask_mail import Mail, Message

app =Flask(__name__)

def configureTheApp(server,port,username,password,tlsBoolean,sslBoolean):
    
    mail=Mail(app)
    app.config['MAIL_SERVER']= server
    app.config['MAIL_PORT'] = port
    app.config['MAIL_USERNAME'] = username
    app.config['MAIL_PASSWORD'] = password
    app.config['MAIL_USE_TLS'] = tlsBoolean
    app.config['MAIL_USE_SSL'] = sslBoolean
    mail = Mail(app)
    return mail



