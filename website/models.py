from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import random
import string

class Quiz(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(255), nullable=False)
  join_code = db.Column(db.String(16), unique=True, nullable=False)
  creator_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  question = db.Column(db.Text)
  option1 = db.Column(db.Text)
  option2 = db.Column(db.Text)
  option3 = db.Column(db.Text)
  option4 = db.Column(db.Text)
  correct_option = db.Column(db.Text)
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())

class Result(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  correct = db.Column(db.SmallInteger)
  incorrect = db.Column(db.SmallInteger)
  percentage = db.Column(db.Float)
  total = db.Column(db.SmallInteger)
  taker_id = db.Column(db.String(150), db.ForeignKey('user.id'))
  quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key should be of type Integer
  username = db.Column(db.String(100), unique=True, nullable=False)
  name = db.Column(db.Text)
  email = db.Column(db.String(150), unique=True, nullable=False)
  password = db.Column(db.Text)
  created_at = db.Column(db.DateTime(timezone=True), default=func.now())
  updated_at = db.Column(db.DateTime(timezone=True), default=func.now())
