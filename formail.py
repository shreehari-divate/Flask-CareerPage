'''
from flask_mail import Mail
from app import app
import os
from dotenv import load_dotenv

load_dotenv()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME']=os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
'''