from flask import render_template
from app import app
from flask import flash,redirect,session
from .forms import LoginForm
from flask import request
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from subprocess import call
import time
import pdb
import MySQLdb
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen

contest=""
class RegistrationForm(Form):
    username = TextField("Username", [validators.Length(min=4, max=20)])
    email = TextField("Email Address", [validators.Length(min=6, max=50)])
    password = PasswordField("Password", [validators.Required(),
                                          validators.EqualTo("confirm", message = "Passwords must match!"),
                                          validators.Length(min=6, max=30)])
    confirm = PasswordField("Repeat Password")


class LoginForm(Form):
    username = TextField("Username")
    password = PasswordField("Password")

def start():
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select max(runid) from runid");
    x=cursor.fetchone()[0];
    runID=x+1;
    return runID

username = ""
user_login = False
ivc = 100000000


@app.route('/source/<source_ID>')
def source_ID(source_ID):
    print source_ID
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select language from runlang where runid=(%s)",(source_ID))
    language = cursor.fetchone()[0]    #different language for each submission
    f = open(str(source_ID) + "." + language)
    x = f.read()
    f.close()
    for y in x:
        print y
    return render_template('source.html' , source_ID = source_ID , x = x , y = x[0])

@app.route('/testing')
def testing():
    data_sent = False
    return render_template('testing.html' , data_sent = data_sent)

@app.route('/generate_testcases' , methods = ['POST'])
def generate_testcases():
   
    print "generate_testcases"
    
    f = open("range_testcases.txt" , "w")
    f.write(str(ivc) + " ")
   
    for i in range(ivc):
        form_name = str(i)
        f.write(request.form[form_name] + " ")
        form_name = str(i + ivc)
        f.write(request.form[form_name] + " ")
   
    f.close()
    call('g++ protest.cpp' ,shell = True)
    call('./a.out')
    call('g++ protest_random.cpp' ,shell = True)
    call('./a.out')

    f = open("labfile.txt" , "r")
    g = open("input_" + testing_problemcode + ".txt" , "w");
    testing_testcases = sum(1 for line in open("labfile.txt"))
    g.write(str(testing_testcases) + "\n")
    g.write(f.read())
    f.close()
    g.close()

    print "file written"


    testing_correct_file = testing_problemcode + "_AC.cpp"
    print testing_correct_file
    testing_output_file = "output_" + testing_problemcode + ".txt"
    print testing_output_file
    call('g++ ' + testing_correct_file , shell = True)
    call('./a.out ' + '< ' + "input_" + testing_problemcode + ".txt" + ' > '  + testing_output_file , shell = True)

    f = open("labfile.txt" , "r")
    boundary_testing = f.read()
    f.close()

    boundary_testing = str(boundary_testing)
    
    print boundary_testing
    
    boundary_testing = boundary_testing.split(' ')
    x = []
    for line in boundary_testing:
        if line >= 0 and line != ' ' and line != '\n':
            x.append(line)

    #print boundary_testing[0]
    #print boundary_testing[1]

    f = open("labfile_random.txt" , "r");
    random_testing = f.read()
    f.close()

    random_testing = random_testing.split(' ')
    
    for line in random_testing:
        if line.strip():           # line contains eol character(s)
            n = int(line)          # assuming single integer on each line
            x.append(n)
    iter = x[0]
    # print random_testing
    return render_template('generate_testcases.html' , x = x , iter = x[0] , ivc = ivc)


@app.route('/create_testcases' , methods = ['POST'])
def create_testcases():
    varcount=request.form['testing_varcount']
    int_varcount = int(varcount)
    problem_code=request.form['testing_problemcode']
   
    global ivc
    ivc = int_varcount
    global testing_problemcode
    testing_problemcode = problem_code
  
    print problem_code
    print varcount
    data_sent = True
    i = 0
    return render_template('testing.html' , data_sent = data_sent , problem_code = problem_code , varcount = int_varcount)


@app.route('/')
@app.route('/index')
def index():
    formReg = RegistrationForm(request.form)
    formLog = LoginForm(request.form)
    # user = {'nickname': 'Dhruv'}  # fake user
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
    return render_template("index.html",title='Home',user=username,problems=problems , user_login = user_login,formReg = formReg, formLog = formLog)

@app.route('/index1')
def index1():
    return render_template("index1.html",user_login=user_login, user=session['username'])

@app.route('/user_profile')
def user_profile():
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select * from users where username =(%s)",(session['username']));
    arr=cursor.fetchall()
    return render_template("user_profile.html",user=session['username'] , arr = arr , x = arr[0]);

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


@app.route('/logout')
def logout():
    global user_login
    user_login = False;
    print hello
    return render_template('index1.html');

@app.route('/contestrankings')
def contestrankings():
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("SELECT username,count(distinct(problem_code)) from contestusers where contest_code=(%s) group by(username) order by(count(distinct(problem_code))) desc",(contest));
    arr=cursor.fetchall()
    for x in arr:
        print str(x[0]+ " " + str(x[1]))
    return render_template("contestrankings.html", arr = arr, x=arr[0],contest=contest)

@app.route('/rankings')
def rankings():
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("SELECT username,count(distinct(problem_code)) from users group by(username) order by(count(distinct(problem_code))) desc");
    arr=cursor.fetchall()
    for x in arr:
        print str(x[0]+ " " + str(x[1]))
    return render_template("rankings.html", arr = arr, x=arr[0])

@app.route('/problems')
def problems():
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select * from contest")
    arr=cursor.fetchall()
    for x in arr:
        print str(x[0]) + " " + str(x[1])
    cnt = 0
    return render_template("problems.html", arr = arr , x = arr[0] , cnt = cnt)

@app.route('/login/' ,methods=['POST'])
def logedin():
    global username
    username = request.form['username']
    passw=request.form['password'];
    session['username']=username;

    global user_login
    user_login = False
    print username;
    print passw;
    # print passw;
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select username from user where password=(%s) and username=(%s)",(passw,session['username']))
	# data=cursor.fetchone()[0]
 #    print data
    # print email
    if int(c) == 0:
        return render_template('service.html')
    else:
        print "query successful"
        data=cursor.fetchone()[0]
        global user_login
        user_login = True
        # session['user']=data;
        return render_template('index1.html' , user_login = user_login , user = session['username'])	

@app.route('/register/', methods=['POST'])
def hello():
	fname=request.form['username'];
	lname=request.form['email'];
	email=request.form['password'];
	passw=request.form['confirm'];
	db = MySQLdb.connect("localhost","root","root","OJ" );
	cursor = db.cursor()
	cursor.execute("insert into user(username,email,password,confirm) values(%s,%s,%s,%s)", (fname,lname,email,passw))
	#data = cursor.fetchone()
	db.commit()
	#print "Database version : %s " % data
	db.close()
	return render_template('hello.html',name=fname);
@app.route('/moretrailers')
def tutorials():
    return render_template("moretrailers.html")
@app.route('/login1')
def login():
    return render_template("login1.html")
@app.route('/at1')
def ATM():
    return render_template("at1.html")

@app.route('/tsort')
def tsort():
    return render_template('tsort.html')

@app.route('/intest')
def intest():
    return render_template('intest.html')

@app.route('/factrl')
def factrl():
    return render_template('factrl.html')

@app.route('/recipe')
def recipe():
	return render_template('recipe.html')
@app.route('/onp')
def onp():
    return render_template('transform.html')
@app.route('/tlg')
def tlg():
    return render_template('tlg.html')
@app.route('/muffin')
def muufn():
    return render_template('muffin.html')

@app.route('/source')
def source():
    return render_template ('source.html')
    
@app.route('/december_long')
def december_long():
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select * from contestproblems")
    arr=cursor.fetchall()
    for x in arr:
        print str(x[0]) + " " + str(x[1]) + " " +str(x[2])
        session['contest']=str(x[3])
        global contest
        contest = session['contest']
    return render_template('december_long.html',arr=arr,x=arr[0],contest=contest)

@app.route('/contest')
def contest():
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select * from contests")
    arr=cursor.fetchall()
    for x in arr:
        print str(x[0]) + " " + str(x[1]) + " " +str(x[2])
        session['contest']=str(x[1])
        global contest
        contest = session['contest']
	return render_template('contests.html', arr=arr,x=arr[0],contest=contest)


"""
@app.route('/problems/<problem>/')
def prob(problem):
	return render_template(problem + '.html'), 200
"""


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
    #all_codes= ['at1','tsort','intest','factrl']         #query
    db = MySQLdb.connect("localhost","root","root","OJ" );
    cursor = db.cursor()
    c=cursor.execute("select code from contest")
    all_codes=[item[0] for item in cursor.fetchall()]
    # print all_codes
    all_languages=['cpp','py','c']
    #pdb.set_trace()
    print ("I got it!")
    data=request.form['projectFilepath']
    problem_code=request.form['problemcode']

    new_code=""
    for c in problem_code:
        if c!=' ':
            new_code+=c
    problem_code=new_code
    print problem_code


    ppproblem_code = []
    ppproblem_code.append(problem_code)
    print "first value"
    print ppproblem_code[0]

    found=False
    for i in range(len(all_codes)):
        print all_codes[i]
        if all_codes[i] == ppproblem_code[0]:
            found=True

    if found==False:
        print "wrong"
    #problem_code=request.form['problem_code']
   
    ###judge logic##
    #print problem_code


    print data
    runID = start()
    print runID
    filename= str(runID)  
    language=str(request.form['problemlanguage'])
    print language

    if language[0] == 'c' and len(language) == 1:
        language = "c"
    elif language[0] == 'c' and language[1] == 'p':
        language = "cpp"
    else:
        language = "py"

   # call('subl ' + filename + '.' + language , shell = True);
    f=open(filename+"."+language,'wt')
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
    f=open(output_file,'w+')

    call('g++ call_me_first.cpp',shell=True);
    call('./a.out > '+output_file,shell=True);
		
    f.close();
    print "hello m don"

    f=open(output_file,'r')
    written_data=f.read()
    print written_data
    f.close()

    print "Code created"
    timelimit=1
    if (language=="cpp") or (language == "c"):
        call('timeout 1s g++ '+filename+"."+language,shell=True);
        print "compliation done"
        start_time=time.time()
        call('timeout 1s ./a.out < '+input_file+' > '+output_file,shell=True);
        duration=time.time()-start_time;
        print duration
        if duration >= timelimit:
            return render_template('result_TLE.html')
    elif(language == "py"):
        start_time=time.time()  
        call('timeout 1s python '+filename+"."+language+' < '+input_file+' > '+output_file,shell=True);
        duration=time.time()-start_time;
        print duration
        if duration >= timelimit:
            return render_template('result_TLE.html')
    else:
        print "Invalid language"
    print "Code created"

    f=open(output_file,'r')
    written_data=f.read()
    f.close()

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

    print "written data"
    print written_data
    print "correct data"
    print correct_data


    if written_data=='compilation error':
        return render_template('result_CE.html')

    print "user submitting is " + str(username)

    if fc1==fc2:
        print "Code is correct"
        print "hello"
        db = MySQLdb.connect("localhost","root","root","OJ" );
        cursor = db.cursor()
        c=cursor.execute("update contest set submissions=submissions+1 where code=(%s)",(problem_code))
        db.commit()
        c=cursor.execute("insert into users (problem_code,source_code,verdict,username) values(%s,%s,%s,%s)", (problem_code,runID,"AC",session['username']))
        db.commit()
        c=cursor.execute("update contestproblems set submissions=submissions+1 where problem_code=(%s)",(problem_code))
        db.commit()
        c=cursor.execute("insert into contestusers (username,problem_code,verdict,contest_code) values(%s,%s,%s,%s)", (session['username'],problem_code,"AC",contest))
        db.commit()
        c=cursor.execute("insert into runid (runid) values(%s)",(runID))
        db.commit()
        c=cursor.execute("insert into runlang values(%s,%s)", (runID,language))
        db.commit()
        db.close()
        return render_template('result_AC.html',duration=duration)
    else:
        print "Code Incorrect"
        return render_template('result_WA.html')
    ##############
    return render_template('trying.html')


"""def login():
    form = LoginForm()
    if request.method=='GET':
        return render_template('login.html',title='Sign_In',form=form)
    elif request.method=='POST':
        print request.form['sing-in-name']   """
