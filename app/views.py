from flask import render_template
from app import app
from flask import flash,redirect
from .forms import LoginForm
from flask import request
from subprocess import call
import time
import pdb
#import requests


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Dhruv'}  # fake user
    problems = [  # fake array of problems
        { 
            'author': {'nickname': 'Yogesh'}, 
            'body': 'Sort an array!' 
        },
        { 
            'author': {'nickname': 'Prakhar'}, 
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
    #pdb.set_trace()
    print ("I got it!")
    data=request.form['projectFilepath']
    problem_code="at1"
    #problem_code=request.form['problem_code']
   
    ###judge logic##
    #print problem_code
    #print data
    filename="runID"    ##create file from input problem_code
    language="cpp"
    f=open(filename+"."+language,'w')
    f.write(str(data))  ##write code from input
    f.close()


    #http://iconizer.net/files/realistiK_Reloaded/orig/error.png

    print data
   
    input_file="input"+"_"+problem_code+".txt"
   
    correct_output_file="output"+"_"+problem_code+".txt"
    f=open(correct_output_file,'r')
    correct_data=f.read()
    f.close()

    output_file="output"+"_"+filename+".txt"
    f=open(output_file,'w')

    call('g++ call_me_first.cpp',shell=True);
    call('/a.out > '+output_file,shell=True);

    f.close();

    f=open(output_file,'r')
    written_data=f.read()
    print written_data
    f.close()

    print "Code created"
    timelimit=1
    if(language=="cpp"):
        call('timeout 1s g++ '+filename+"."+language,shell=True);
        print "compliation done"
        start_time=time.time()
        call('timeout 1s ./a.out < '+input_file+' > '+output_file,shell=True);
        duration=time.time()-start_time;
        print duration
        if duration >= timelimit:
            return render_template('result_TLE.html')

    print "Code created"

    f=open(output_file,'r')
    written_data=f.read()
    f.close()

    print written_data
    print correct_data

    if written_data=='compilation error':
        return render_template('result_CE.html')

    if written_data==correct_data:
        print "Code is correct"
        return render_template('result_AC.html',duration=duration)
    else:
        print "Code Incorrect"
        return render_template('result_WA.html')
    ##############
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
