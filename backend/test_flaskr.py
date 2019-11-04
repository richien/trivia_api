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
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_user, self.database_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # add a question and category to the test database
            self.category = Category(type='Asia')
            self.question = Question(
                question='Where is China?',
                answer='In Asia',
                category=1,
                difficulty=2)
            self.db.session.add(self.category)
            self.db.session.add(self.question)
            self.db.session.commit()
    
    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.session.delete(self.question);
            self.db.session.delete(self.category);
            self.db.session.commit()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_questions_with_successfull_response(self):
        response = self.client().get('/api/v1/questions?page=1')
        data = json.loads(response.data)

        self.assertTrue(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 1)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(len(data['categories']), 1)
        self.assertIsNone(data['current_category'])
    
    def test_get_questions_with_unsuccessfull_response(self):
        with self.app.app_context():
            self.db.session.delete(self.question);
            self.db.session.commit()

        response = self.client().get('/api/v1/questions?page=1000')
        data = json.loads(response.data)

        self.assertTrue(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()