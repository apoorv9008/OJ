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
#@app.route('/index')
def index():
    return render_template("home.html")
