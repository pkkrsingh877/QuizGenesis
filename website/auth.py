from flask import Blueprint, render_template

auth = Blueprint('auth', '__name__')

@auth.route('/login', methods=['GET','POST'])
def login():
    return render_template('auth/login.html')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('auth/signup.html')

@auth.route('/signout', methods=['GET','POST'])
def signout():
    return "<h1>Log out</h1>"