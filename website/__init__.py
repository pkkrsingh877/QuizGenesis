from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") #Encrypts Cookies and Sessions
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getenv("DB_NAME")}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .quiz import quiz

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(quiz, url_prefix='/quiz')
    
    from .models import User, Quiz, Question, Result

    create_database(app)

    return app

def create_database(app):
    from . import db  # Importing db inside the function to ensure it's within the application context
    with app.app_context():
        if not os.path.exists('instance/' + os.getenv('DB_NAME')):
            db.create_all()
            print("Created Database")


create_app()