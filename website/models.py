from . import db
from flask_login import UserMixin
import random
import string

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    join_code = db.Column(db.String(16), unique=True, nullable=False, default=''.join(random.choices(string.ascii_uppercase + string.digits, k=16)))
    questions = db.relationship('Question', backref='quiz', lazy=True)
    users = db.relationship('User', backref='quiz_ref', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text)
    option1 = db.Column(db.Text)
    option2 = db.Column(db.Text)
    option3 = db.Column(db.Text)
    option4 = db.Column(db.Text)
    correct_option = db.Column(db.Text)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

    # Define relationship with Quiz model
    quiz = db.relationship("Quiz", back_populates="questions")

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    correct = db.Column(db.SmallInteger)
    incorrect = db.Column(db.SmallInteger)
    percentage = db.Column(db.Float)
    total = db.Column(db.SmallInteger)
    username = db.Column(db.String(150), db.ForeignKey('user.username'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))


class User(db.Model, UserMixin):
    username = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Text)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text)
    results = db.relationship('Result')
    quizzes = db.relationship('Quiz')
