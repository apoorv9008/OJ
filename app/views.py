from flask import render_template
from app import app
from flask import flash,redirect
from flask import request
from subprocess import call
import time
import pdb
from bs4 import BeautifulSoup
from urllib2 import urlopen
#import requests

@app.route('/clist')
def clist():
    url=urlopen("http://clist.by/")
    soup = BeautifulSoup(url)
    x = []
    y = []
    for link in soup.find_all('div' , class_ = "contest-title"):
        x.append(link.a["title"])
        y.append(link.a["href"])
        # print link.a["title"]
        # print link.a["href"]
    return render_template("clist.html" , cnames = x , clinks = y , item = x[0])

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

@app.route('/check')
def check():
    return render_template('extend.html')

@app.route('/problems')
def problems():
    return render_template("problems.html")

"""@app.route('/ATM')
def ATM():
    return render_template("atm.html")

@app.route('/tsort')
def tsort():
    return render_template('tsort.html')

@app.route('/intest')
def intest():
    return render_template('intest.html')
"""
@app.route('/problems/<problem>')
def prob(problem):
    page_name=problem+'.html'
    return render_template(page_name)

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

    all_codes= ['at1','tsort','intest']

    #pdb.set_trace()
    print ("I got it!")
    data=request.form['projectFilepath']
    problem_code=request.form['problemcode']

    new_code=""
    for c in problem_code:
        if c!=' ' and c != '\n':
            new_code+=c
    problem_code=new_code
    
    print problem_code

    found=False
    for codes in all_codes:
        if codes == problem_code:
            found = True

    if found == False:
        return render_template('invalid problem code.html')

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

    # print data
   
    input_file="input"+"_"+problem_code+".txt"
   
    correct_output_file="output"+"_"+problem_code+".txt"
    f=open(correct_output_file,'r')
    correct_data=f.read()
    f.close()

    output_file="output"+"_"+filename+".txt"
    f=open(output_file,'w')

    call('g++ call_me_first.cpp',shell=True);
    call('./a.out > '+output_file,shell=True);

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

    # print written_data
    # print correct_data

    print "checking"
    check1 = ""
    check2 = ""    
    for item in written_data:
        check1 += str(item)

    for item in correct_data:
        check2 += str(item)

    # print check1
    # print check2

    fc1 = ""
    fc2 = ""
    for x in check1:
        x = str(x)
        if ( (x >= 'a' and x <= 'z') or (x >= '0' and x <= '9') or (x >= 'A' and x <= 'Z')):
            fc1 += x

    for x in check2:
        x = str(x)
        if ( (x >= 'a' and x <= 'z') or (x >= '0' and x <= '9') or (x >= 'A' and x <= 'Z')):
            fc2 += x

    print fc1
    print fc2

    # print correct_data

    if written_data=='compilation error':
        return render_template('result_CE.html')

    if fc1 == fc2:
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
