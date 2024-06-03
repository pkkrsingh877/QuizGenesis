from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Quiz, Question, Result
from .modules.generate_join_code import generate_join_code

from flask_login import login_required, current_user

quiz = Blueprint('quiz', '__name__')

@quiz.route('/')
@login_required
def index():
    quiz = Quiz.query.filter_by(creator_id=current_user.id).all()

    if quiz:
        print(quiz)
        print(current_user.id)
    # Pass quiz name and questions to the template
    return render_template('quiz/index.html', user=current_user, quizzes=quiz)

@quiz.route('/join', methods = ['GET','POST'])
@login_required
def join():
    if request.method == 'GET':
        return render_template('quiz/join_quiz.html', user=current_user)
    else:
        # Get Join Code from User Form
        join_code = request.form.get('join_code')
        quiz = Quiz.query.filter_by(join_code=join_code).first()

        if quiz:
            # Retrieve questions associated with the quiz
            questions = Question.query.filter_by(quiz_id=quiz.id).all()

            if questions:
                # Pass quiz name and questions to the template
                return render_template('quiz/attempt_quiz.html', quiz_name=quiz.name, questions=questions, user=current_user)
        
        flash("Incorrect Join Code", category="failure")
        return redirect(url_for('quiz.join'))

@quiz.route('/create', methods = ['GET','POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('quiz/create.html', user=current_user)
    else:
        quiz_name = request.form.get('quiz_name')
        questions = request.form.getlist('question[]')
        options = request.form.getlist('option[]')
        correct_options = request.form.getlist('correct_option[]')

        # Create a new quiz instance
        new_quiz = Quiz(name=quiz_name,join_code=generate_join_code(),creator_id=current_user.id)
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
        
        return redirect(url_for('quiz.index'))

@quiz.route('/submit', methods=['POST'])
@login_required
def submit():
    # Retrieve all answers from the form
    answers = request.form.to_dict()
    correct = 0
    incorrect = 0
    total_questions = 0

    # Iterate over each answer submitted
    for key, user_answer in answers.items():
        if key.startswith('answers['):
            question_id = key[8:-1]  # Extract question ID from key, e.g., 'answers[12]' -> '12'
            question = Question.query.get(question_id)
            if question and user_answer == question.correct_option:
                correct += 1
            else:
                incorrect += 1
            total_questions += 1
    
    # Calculate the percentage
    if total_questions > 0:
        percentage = (correct / total_questions) * 100
    else:
        percentage = 0

    # Create and save the result to the database
    new_result = Result(
        correct= correct,
        incorrect=incorrect,
        percentage=percentage,
        total=total_questions,
        taker_id=current_user.id,
        quiz_id=question.quiz_id if question else None
    )
    db.session.add(new_result)
    db.session.commit()
    
    quiz = Quiz.query.get(new_result.quiz_id)
    return render_template('quiz/results.html', correct=correct, total_questions=total_questions, percentage=percentage, user=current_user, quiz_name=quiz.name if quiz else None)