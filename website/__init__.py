from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") #Encrypts Cookies and Sessions
    
    from .views import views
    from .auth import auth
    from .quiz import quiz

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(quiz, url_prefix='/quizzes')
    
    return app

create_app()