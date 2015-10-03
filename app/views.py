from flask import render_template
from app import app
from flask import flash,redirect
from .forms import LoginForm
from flask import request
#import requests


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Dhruv'}  # fake user
    problems = [  # fake array of problems
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Sort an array!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'Count even numbers!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           problems=problems)


@app.route('/problems')
def problems():
    return render_template("problems.html")

@app.route('/ATM')
def ATM():
    return render_template("atm.html")

"""@app.route('/submit')
def submit():
    return render_template("submit.html")
"""

@app.route('/submit')#,methods=['GET','POST'])
def submit():
    #print ("I got it!")
    #print request.form['projectFilepath']
    return render_template('submit.html')

@app.route('/trying',methods=['POST'])
def trying():
    print ("I got it!")
    print request.form['projectFilepath']
    return render_template('trying.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    #print "HELLO"
        #will stay on the same page if field is empty
    if ( form.validate_on_submit() ):
        flash('Login requested form ID="%s" ' %(form.openid.data))
        print form.openid.data
        return redirect('/index')
    return render_template('login.html',title="Sign-In",form=form)
"""def login():
    form = LoginForm()
    if request.method=='GET':
        return render_template('login.html',title='Sign_In',form=form)
    elif request.method=='POST':
        print request.form['sing-in-name']   """
