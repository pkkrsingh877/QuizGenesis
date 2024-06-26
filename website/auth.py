from flask import redirect, Blueprint, render_template, request, flash, url_for
from website.modules.validate_password import validate_password
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_user, logout_user, login_required, current_user

from . import db   ##means from __init__.py import db
from .models import User

auth = Blueprint('auth', '__name__')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html', user=None)
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        if not validate_password(password):
            flash("1 uppercase, 1 lowercase, 1 digit, min length = 8, max length = 20, 1 special character",  category="failure")
            return redirect('/')
        elif username == "":
            flash("Username can't be empty", category="failure")
            return redirect('/')
        else:
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    flash("User Logged In", category="success")
                    return redirect(url_for('views.home'))
    flash("Invalid Username/Password", category="failure")
    return redirect(url_for('auth.login'))
            

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html', user=None)
    else:
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username not available")
        elif not validate_password(password):
            flash("1 uppercase, 1 lowercase, 1 digit, min length = 8, max length = 20, 1 special character",  category="failure")
        elif len(email) < 6:
            flash("Email must be of length greater than 6",  category="failure")
        elif name == "":
            flash("Name can't be empty", category="failure")
        elif username == "":
            flash("Username can't be empty", category="failure")
        else:
            newUser = User(username=username, password=generate_password_hash(password), name=name, email=email)
            db.session.add(newUser)
            db.session.commit()
            flash("Account Created & User Logged In", category="success")
            user = newUser
            login_user(user, remember=True)

    return redirect(url_for('views.home'))

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    flash('User Logged Out', category="success")
    return redirect(url_for('auth.login'))