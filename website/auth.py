from flask import redirect, Blueprint, render_template, request, flash
from website.modules.validate_password import validate_password

auth = Blueprint('auth', '__name__')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if not validate_password(password):
            flash("1 uppercase, 1 lowercase, 1 digit, min length = 8, max length = 20, 1 special character",  category="failure")
        elif username == "":
            flash("Username can't be empty", category="failure")
        else:
            flash("Login Successful", category="success")

    return redirect('/')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    else:
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not validate_password(password):
            flash("1 uppercase, 1 lowercase, 1 digit, min length = 8, max length = 20, 1 special character",  category="failure")
        elif len(email) < 6:
            flash("Email must be of length greater than 6",  category="failure")
        elif name == "":
            flash("Name can't be empty", category="failure")
        elif username == "":
            flash("Username can't be empty", category="failure")
        else:
            flash("Account Created", category="success")

    return redirect('/')

@auth.route('/signout', methods=['GET','POST'])
def signout():
    return "<h1>Log out</h1>"