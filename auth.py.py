from flask import Flask,redirect,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
import bcrypt

from datetime import datetime


app=Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///disastermanagement.db'


db=SQLAlchemy(app)

app.secret_key="fjhfweoiddjhsljqwld87e837iuhfkjvas//"

class Notes(db.Model):
    id= db.Column('id',db.Integer ,primary_key=True )
    userid= db.Column('userid',db.String(50),nullable=False)
    
    notedesc=db.Column('notedesc',db.String(250),nullable=False)


class Users(db.Model):
    id = db.Column('id',db.Integer ,primary_key=True )
    name = db.Column("name",db.String(50),nullable=False,) 
    email = db.Column("email",db.String(50),unique=True,nullable=False)  
    password = db.Column("password",db.String(50),nullable=False)
    date_created =db.Column(db.DateTime, default=datetime.now(),nullable=True)


    def __init__(self,name,email,password):

        self.name=name
        self.email=email
        self.password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    def check_pass(self,password):  

        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    

with app.app_context():
    db.create_all()

@app.route('/signup',methods=['GET','POST'])

def signup():
        
    if request.method=="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')

        new_user=Users(name=name,email=email,password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template('signup.html')




@app.route('/login',methods=['GET','POST'])

def login():

    if 'user' in session:
        return redirect("/")
    
    elif request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user=Users.query.filter_by(email=email).first()

        if user and Users.check_pass:

            session['user']=user.email

            return redirect("/")




    return render_template('login.html')





@app.route('/logout')
def logout():
    
        
    
    session.pop('user',None)

    
    return redirect('/login')


@app.route('/')

def home():

    if 'user' in session:
    
        return "logged in"
    return redirect('/login')


if __name__=="__main__":
    app.run(debug=True)