import json
from flask import Flask, request, abort, jsonify, Blueprint

from ..models import db, Question, Category
from .helpers import isValidQuestion


QUESTIONS_PER_PAGE = 10

question = Blueprint('question', __name__)
'''
Endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint returns a list of questions,
number of total questions, current category, categories.
'''
@question.route('/questions', methods=['GET'])
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
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'categories': [category.format() for category in categories],
            'total_questions': total_questions[0].total,
            'current_category': None
        }), 200
    except Exception as error:
        raise error
    finally:
        db.session.close()


'''
Endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.
'''
@question.route('/questions', methods=['POST'])
def add_new_question():
    try:
        data = json.loads(request.data)
        if not isValidQuestion(data):
            abort(400)
        question = Question(**data)
        db.session.add(question)
        db.session.commit()
        return jsonify({
            'success': True,
            'data': question.format()
        }), 201
    except Exception as error:
        raise error
    finally:
        db.session.close()


'''
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
'''
@question.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    try:
        question = Question.query.get(id)
        if question is None:
            abort(422)
        db.session.delete(question)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Question with ID: {id} deleted'
        }), 200
    except Exception as error:
        raise error
    finally:
        db.session.close()


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
        return jsonify({
            'success': True,
            'categories': [category.format() for category in categories]
        }), 200
    except Exception as error:
        raise error
    finally:
        db.session.close()


'''
Endpoint to get questions based on category.
'''
@question.route('/categories/<int:id>/questions')
def retrieve_questions_by_category(id):
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', QUESTIONS_PER_PAGE, type=int)
        offset = (page - 1) * limit
        questions = Question.query.filter_by(
            category=str(id)).offset(offset).limit(limit).all()
        if not questions:
            abort(404)
        category = Category.query.get(id)
        total_questions = db.session.query(
            db.func.count(Question.id).label('total')
            ).filter_by(category=str(id)).all()
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': total_questions[0].total,
            'current_category': category.format()
        }), 200
    except Exception as error:
        raise error
    finally:
        db.session.close()
