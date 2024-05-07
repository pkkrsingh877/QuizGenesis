from flask import Blueprint, render_template

'''
So basically Blueprint is used to create routes
and we can use the name of blueprint to create
routes that go within that blueprint.
'''

views = Blueprint('views', '__name__')

@views.route('/')
def home():
    return render_template('home/index.html')
