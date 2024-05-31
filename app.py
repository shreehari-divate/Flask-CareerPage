from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='asdf123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:s1906@localhost/cpage'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    phno = db.Column(db.Integer,nullable=False,unique=True)
    quali = db.Column(db.String(20),nullable=False)
    spec = db.Column(db.String(20),nullable=False)
    skills = db.Column(db.String(20),nullable=False)
    exp = db.Column(db.Integer,nullable=False)
    avail = db.Column(db.Integer,nullable=False)
    cur_sal = db.Column(db.Integer,nullable=False)
    exp_sal = db.Column(db.Integer,nullable=False)

class JobPos(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),nullable=False)
    exp = db.Column(db.Integer,nullable=False)
    sal = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String(20),nullable=False)


@app.route("/",methods=['GET','POST'])
def home():
    job_pos = JobPos.query.all()
    return render_template("home.html",job_pos=job_pos)

@app.route("/apply",methods=['GET','POST'])
def apply():
       
    return render_template("application.html")

#driver code:
if __name__=="__main__":
    app.run(debug=True)