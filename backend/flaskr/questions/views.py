from flask import Flask, request, abort, jsonify, Blueprint

from flaskr.models import db, Question, Category


QUESTIONS_PER_PAGE = 10

question = Blueprint('question', __name__)
'''
  Endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint returns a list of questions,
  number of total questions, current category, categories.
'''
@question.route('/questions')
def retrieve_questions():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
    offset = (page - 1) * limit
    try:
        questions = Question.query.offset(offset).limit(limit).all()
        if not questions:
            abort(404)
        categories = Category.query.all()
        total_questions = db.session.query(
            db.func.count(Question.id).label('total')).all()
    except Exception as error:
        raise error
    return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'categories': [category.format() for category in categories],
        'total_questions': total_questions[0].total,
        'current_category': None
    })

'''
Endpoint to handle GET requests
for all available categories.
'''
@question.route('/categories')
def retrieve_categories():
    try:
        categories = Category.query.all()
        if not categories:
            abort(404)
    except Exception as error:
        raise error
    return jsonify({
        'success': True,
        'categories': [category.format() for category in categories]
    })
