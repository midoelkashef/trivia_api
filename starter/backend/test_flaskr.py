import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:123@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_question = {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            }

            self.play_quizzes_input = {
                "previous_questions": [],
                "quiz_category": {"type": "History", "id": 4}
            }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000', json={'gategory': 4})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_gategory(self):
        res = self.client().get('/categories/7', json={'gategory': 'Art'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_beyond_valid_question(self):
        res = self.client().get('/question/27', json={'gategory': '1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client().delete('/questions/15')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == 15).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 15)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_405_if_add_question_not_allowed(self):
        res = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not allowed')

    def test_search_question(self):
        res = self.client().post('/questions/search', json={"search": "what"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_if_search_is_empety(self):
        res = self.client().post('/questions/search', json={"search": ""})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_questions_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_if_category_does_not_exist(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable To Process Request')

    def test_play_quizzes(self):
        res = self.client().post('/quizzes', json=self.play_quizzes_input)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_400_if_no_category_id(self):
        res = self.client().post(
            '/quizzes', json={"quiz_category": {"type": "Art", "id": 0}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

        # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
