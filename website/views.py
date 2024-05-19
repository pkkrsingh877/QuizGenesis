from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_required, current_user

from . import db 
from .models import User

views = Blueprint('views', '__name__')

@views.route('/')
@login_required
def home():
    return render_template('home/index.html', user=current_user)

@views.route('/view_profile')
@login_required
def view_profile():
    return render_template('user/view_profile.html', user=current_user)

@views.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'GET':
        return render_template('user/update_profile.html', user=current_user)
    else:
        user = User.query.filter_by(username=current_user.username).first()

        if not user:
            flash('User not found')
            return redirect(url_for('views.home'))
        
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Update only the fields that are provided
        if name:
            user.name = name
        if email:
            user.email = email
        if username:
            user.username = username
        if password:  # Only update password if it is provided
            user.password = password
            flash('You are not allowed to update password...')
            return redirect(url_for('auth.login'))
        
        # Save changes to the database
        db.session.commit()

        flash('Profile updated successfully')
        return redirect(url_for('views.view_profile'))

@views.route('/delete_profile')
@login_required
def delete_profile():
    # This will allow users to delete their account
    user = User.query.filter_by(username=current_user.username).first()

    if not user:
        flash('User not found')
        return redirect(url_for('views.home'))
    
    db.session.delete(user)
    db.session.commit()

    flash('Account Deleted Successfully')
    return redirect(url_for('auth.signup'))
