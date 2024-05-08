from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Quiz, Question 
from .modules.generate_join_code import generate_join_code

quiz = Blueprint('quiz', '__name__')

@quiz.route('/')
def index():
    return render_template('quiz/index.html')

@quiz.route('/join', methods = ['POST'])
def join():

    # Get Join Code from User Form
    join_code = request.form.get('join_code')

    quiz = Quiz.query.filter_by(join_code=join_code).first()

    if quiz:
        # Retrieve questions associated with the quiz
        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        print(questions)
        for question in questions:
            print(question.question)
            print("Option 1", question.option1)
            print("Option 2", question.option2)
            print("Option 3", question.option3)
            print("Option 4", question.option4)
    
    return "<div>Join Code reaching backend successfully</div>"

@quiz.route('/create', methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('quiz/create.html')
    else:
        quiz_name = request.form.get('quiz_name')
        questions = request.form.getlist('question[]')
        options = request.form.getlist('option[]')
        correct_options = request.form.getlist('correct_option[]')

        # Create a new quiz instance
        new_quiz = Quiz(name=quiz_name,join_code=generate_join_code())
        db.session.add(new_quiz)
        db.session.commit()

        # Create question instances and associate them with the quiz
        for i, question_text in enumerate(questions):
            option1 = options[i*4]
            option2 = options[i*4 + 1]
            option3 = options[i*4 + 2]
            option4 = options[i*4 + 3]
            correct_option = correct_options[i]

            new_question = Question(
                question=question_text,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correct_option=correct_option,
                quiz_id=new_quiz.id
            )
            db.session.add(new_question)
        
        # Commit changes to the database
        db.session.commit()
        
        return f"<div>Data Recieved by backend <br> Join Code is {new_quiz.join_code} </div>"
