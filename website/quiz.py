from flask import Blueprint, render_template


quiz = Blueprint('quiz', '__name__')

@quiz.route('/')
def join():
    return render_template('home/join.html')
