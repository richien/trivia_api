import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv('TEST_DATABASE_NAME')
        self.database_user = os.getenv('DATABASE_USER')
        self.database_password = os.getenv('DATABASE_PASSWORD')
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.database_user,
            self.database_password,
            'localhost:5432',
            self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # add a question to a category in the test database
            self.category = Category(type='Asia')
            self.db.session.add(self.category)
            self.db.session.flush()
            self.question = Question(
                question='Where is China?',
                answer='In Asia',
                category=self.category.id,
                difficulty=2)
            self.db.session.add(self.question)
            self.db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        # delete all questions and categories in the test database
        # and close the session
        with self.app.app_context():
            self.db.session.query(Question).delete()
            self.db.session.query(Category).delete()
            self.db.session.commit()
            self.db.session.close()

    def test_get_questions_with_successfull_response(self):
        response = self.client().get('/api/v1/questions?page=1')

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(len(data['categories']), 1)
        self.assertIsNone(data['current_category'])

    def test_get_questions_with_failure_response(self):
        # if there are no questions found, return a 404 error response
        with self.app.app_context():
            self.db.session.delete(self.question)
            self.db.session.commit()

        response = self.client().get('/api/v1/questions?page=1000')
        data = json.loads(response.data)

        self.assertTrue(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_categories_with_successfull_response(self):
        response = self.client().get('/api/v1/categories')

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 1)

    def test_get_categories_with_failure_response(self):
        # if there are no categories found, return a 404 error response
        with self.app.app_context():
            self.db.session.delete(self.category)
            self.db.session.commit()

        response = self.client().get('/api/v1/categories')
        data = json.loads(response.data)

        self.assertTrue(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_questions_by_category_with_successfull_response(self):
        category = Category.query.first()
        response = self.client().get(
            '/api/v1/categories/{}/questions'.format(category.id))

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], category.format())

    def test_get_questions_by_category_with_failure_response(self):
        invalid_id = 0
        response = self.client().get(
            '/api/v1/categories/{}/questions'.format(invalid_id))

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_add_question_with_success_response(self):
        response = self.client().post(
            '/api/v1/questions',
            content_type='application/json',
            data=json.dumps({
                'question': 'What is the longest river in Asia?',
                'answer': 'Yangtze River',
                'difficulty': 1,
                'category': 1
            })
        )

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(
            data['data']['question'],
            'What is the longest river in Asia?')

    def test_add_question_with_invalid_field_in_body(self):
        response = self.client().post(
            '/api/v1/questions',
            content_type='application/json',
            data=json.dumps({
                'question': 'What is the longest river in Asia?',
                'anwer': 'Yangtze River',
                'difficulty': 1,
                'category': 1
            })
        )

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_add_question_with_empty_field_in_body(self):
        response = self.client().post(
            '/api/v1/questions',
            content_type='application/json',
            data=json.dumps({
                'question': 'What is the longest river in Asia?',
                'answer': '',
                'difficulty': 1,
                'category': 1
            })
        )

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_add_question_with_missing_field_in_body(self):
        response = self.client().post(
            '/api/v1/questions',
            content_type='application/json',
            data=json.dumps({
                'question': 'What is the longest river in Asia?',
                'difficulty': 1,
                'category': 1
            })
        )

        data = json.loads(response.data)

        self.assertTrue(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_body_of_delete_question_for_successfull_request(self):
        question = Question.query.first()

        response = self.client().delete(f'/api/v1/questions/{question.id}')
        data = json.loads(response.data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'])

    def test_question_is_deleted_successfully(self):
        len_db_before = len(Question.query.all())
        question = Question.query.first()

        self.client().delete(f'/api/v1/questions/{question.id}')
        len_db_after = len(Question.query.all())

        self.assertNotEqual(len_db_before, len_db_after)

    def test_error_body_on_failure_to_delete_question(self):
        wrong_id = 101010

        response = self.client().delete(f'/api/v1/questions/{wrong_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unable to process request')

    def test_body_of_search_response_for_successfull_request(self):
        search_term = 'china'

        response = self.client().post(
            '/api/v1/questions',
            content_type='application/json',
            data=json.dumps({
                'searchTerm': search_term
            }))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['current_category'], None)

    def test_error_body_for_searchtearm_with_empty_string(self):
        search_term = ''

        response = self.client().post(
            '/api/v1/questions',
            content_type='application/json',
            data=json.dumps({
                'searchTerm': search_term
            }))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_get_quiz_question_without_previous_questions(self):
        response = self.client().post(
            '/api/v1/quizzes',
            content_type='application/json',
            data=json.dumps({
                'previous_questions': [],
                'quiz_category': {'id': 0, 'type': 'all'}
            }))

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

    def test_get_quiz_question_with_previous_questions(self):
        # add an additional question so that there is
        # more than one question in the database
        with self.app.app_context():
            category = Category.query.first()
            new_question = Question(
                question='Where is England?',
                answer='In Europe',
                category=category.id,
                difficulty=1)
            self.db.session.add(new_question)
            self.db.session.commit()
        question = Question.query.first()
        response = self.client().post(
            '/api/v1/quizzes',
            content_type='application/json',
            data=json.dumps({
                'previous_questions': [question.id],
                'quiz_category': {'id': 0, 'type': 'all'}
            }))

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['id'] != question.id)

    def test_get_quiz_question_with_no_more_questions_available(self):
        questions = Question.query.all()
        response = self.client().post(
            '/api/v1/quizzes',
            content_type='application/json',
            data=json.dumps({
                'previous_questions': [question.id for question in questions],
                'quiz_category': {'id': 0, 'type': 'all'}
            }))

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_quiz_question_with_invalid_request_body(self):
        question = Question.query.first()
        response = self.client().post(
            '/api/v1/quizzes',
            content_type='application/json',
            data=json.dumps({
                'previous_questions': [question.id]
            }))

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
