from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Quiz, Question 
from .modules.generate_join_code import generate_join_code

quiz = Blueprint('quiz', '__name__')

@quiz.route('/')
def join():
    # Retrieve the first quiz from the database
    quiz = Quiz.query.first()
    print("Quiz:")
    print(quiz.id, quiz.name)  # Print quiz attributes individually for better readability

    # Retrieve questions associated with the quiz
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    print(questions)
    print("Questions:")
    for question in questions:
        print(question.id, question.question, question.option1, question.option2, question.option3, question.option4, question.correct_option)  # Print question attributes individually
    return render_template('quiz/join.html')

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
        
        return "<div>Data Recieved by backend</div>"
