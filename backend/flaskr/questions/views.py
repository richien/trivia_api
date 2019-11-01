from flask import Flask, request, abort, jsonify, Blueprint

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

question = Blueprint('question', __name__)

@question.route('/questions')
def questions():
    return jsonify({
        'success': True,
        'questions': 'Hello World'
    })