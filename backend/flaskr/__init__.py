from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .models import setup_db


api_url_prefix = '/api/v1'
# load environment variables
load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # register blue prints for routes
    from .questions.views import question

    app.register_blueprint(question, url_prefix=api_url_prefix)

    # set up CORS
    CORS(app, resource={r'/api/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response

    # application error handlers

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': 'unable to process request'
        }), 422

    return app

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
          'success': False,
          'error': 500,
          'message': 'internal server error'
        }), 500

    return app
