import os
import smtplib
from flask import Flask, redirect, render_template, request, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from fileinput import filename
from dotenv import load_dotenv
from flask_wtf.csrf import generate_csrf
load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME']=os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    phno = db.Column(db.String(20),nullable=False,unique=True)
    quali = db.Column(db.String(20),nullable=False)
    spec = db.Column(db.String(20),nullable=False)
    skills = db.Column(db.String(100),nullable=False)
    exp = db.Column(db.Integer,nullable=False)
    avail = db.Column(db.Integer,nullable=False)
    cur_sal = db.Column(db.Integer,nullable=False)
    exp_sal = db.Column(db.Integer,nullable=False)
    filename = db.Column(db.String(20),nullable=False)
    file = db.Column(db.LargeBinary)

class JobPos(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    exp = db.Column(db.Integer,nullable=False)
    sal = db.Column(db.String(20),nullable=False)
    location = db.Column(db.String(20),nullable=False)
    description = db.relationship('JobDesc',backref='job_pos',uselist=False) #this defines a reltionship btwn JobPos and JobDesc. 
    #backref adds job_desc attribute to JobDesc instance, which will return JobPos instance that JobDesc is related to.
    #uselist=False is to define one-to-one relationship. If True it is one-to-many.

class JobDesc(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer,db.ForeignKey('job_pos.id'), nullable=False) #job_pos.id is a foreign key refering to id column of job_pos table. This creates link between JobPos and JobDesc
    desc = db.Column(db.Text,nullable=False)
    resp = db.Column(db.Text,nullable=False)
    qualif = db.Column(db.Text,nullable=False)
    pref_skills = db.Column(db.Text,nullable=False)

@app.route("/",methods=['GET','POST'])
def home():
    job_pos = JobPos.query.all()
    return render_template("home.html",job_pos=job_pos)

@app.route("/apply/<job_title>",methods=['GET','POST'])
def apply(job_title):
    job_desc=JobPos.query.filter_by(title=job_title).first()   
    #print(job_desc)
    #print(job_desc.description)
    csrf_token = generate_csrf()


    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phno=request.form.get('phno')
        quali=request.form.get('quali')
        spec=request.form.get('spec')
        skills=request.form.get('skills')
        exp=request.form.get('exp')
        avail=request.form.get('avail')
        cur_sal=request.form.get('cur_sal')
        exp_sal=request.form.get('exp_sal')
        files=request.files['res']
        
        user_exists = User.query.filter((User.email==email) | (User.phno==phno)).first()
        if user_exists:
            msg = 'User already exits'
            return render_template('application.html',msg=msg,job_desc=job_desc)
        
        if name and email and phno and quali and spec and skills and exp and avail and cur_sal and exp_sal:

            user = User(role=job_title,name=name,email=email,phno=phno,
                        quali=quali,spec=spec,skills=skills,exp=exp,
                        avail=avail, cur_sal=cur_sal,exp_sal=exp_sal,
                        filename=files.filename,file=files.read()
                        )
            db.session.add(user)
            db.session.commit()
            print('Data has been stored successfully')
            try:
                message = Message('Application recieved',sender=os.getenv('MAIL_USERNAME'),recipients=[email])
                message.body=f'Thank You {name} for showing your interest at Yashodha Technologies for {job_title} role.\nWe have recieved your application and will get back to you as soon as possible.\n\nRegards,\nYashodha Technologies LTD'
                mail.send(message)
            except smtplib.SMTPAuthenticationError:
                print("SMTP Auth error has occured")
            return redirect(url_for('success',name=name))

    return render_template("application.html",job_desc=job_desc,csrf_token=csrf_token)

@app.route('/success<name>')
def success(name):
    return render_template('thankyou.html',name=name)

#driver code:
if __name__=="__main__":
    app.run(debug=True)