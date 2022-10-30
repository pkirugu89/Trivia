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
        self.db_host = os.getenv('db_host','127.0.0.1:5432')
        self.db_user = os.getenv('db_user','student')
        self.db_code = os.getenv('db_code', 'student')
        self.database_name = "trivia_test"
        self.database_path = "postgresql+psycopg2://{}:{}@{}/{}".format(self.db_user,self.db_code,self.db_host, self.database_name)
        # new question test
        self.new_question ={
            'id':26,
            'question':'test question',
            'answer': 'test answer',
            'difficulty':3,
            'category':1
        }
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    # test for retrieving all categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']),6)
        self.assertIsInstance(data['categories'], dict)
    # retrieve all questions
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data= json.loads(res.data)
        # status code
        self.assertEqual(res.status_code,200)  
        self.assertEqual(data['success'],True)
        #questions
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'],list)
        self.assertEqual(len(data['questions']),10)
        # total questions
        self.assertEqual(data['total_questions'],22)
        # categories  
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']),6)
        self.assertIsInstance(data['categories'],dict)
        self.assertEqual(data['current_category'], None)
    # # create question test
    # def test_create_question(self):
    #     res = self.client().post('/create_question', json = self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['created'],26)
    # delete question test
    # def test_delete_questions(self):
    #     res = self.client().delete('/questions/25')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code,200)
    #     self.assertEqual(data['success'],True)
    #     self.assertEqual(data['deleted'],25)
    # 404 delete question error test
    def test_422_delete_not_valid_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    # search question test
    def test_search_question(self):
        res = self.client().post('/search',json={'searchTerm': 'Taj Mahal'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'],list)
        self.assertEqual(len(data['questions']),1)
        self.assertEqual(data['total_questions'],1)
   
    # search question without results
    def test_search_question_without_results(self):
        res = self.client().post('/search',json={'searchTerm': 'xxxx'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertIsInstance(data['questions'],list)
        self.assertEqual(len(data['questions']),0)
        self.assertEqual(data['total_questions'],0)
  
    # get questions by category test
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])

        self.assertIsInstance(data['questions'],list)
        self.assertEqual(len(data['questions']),6)
        self.assertEqual(data['total_questions'],6)
        #self.assertEqual(data['current_category'],1)
    # 404 questions without category test
    def test_404_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'Resource Not Found')
    
    # testing quizzes with both category and previous questions
    def test_quizzes_with_category_with_previous_questions(self):
        res = self.client().post('/quizzes', json={
            'previous_questions':[],
            'quiz_category':{
                'id':'1',
                'type':'Science'
            }
        })
        data = json.loads(res.data)
        # status code
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertIsInstance(data['question'],dict)
    
    # testing quizzes with categories and some previous questions
    def test_quizzes_with_category_withsome_previous_questions(self):
        res = self.client().post('quizzes', json= {
            'previous_questions':[21,22],
            'quiz_category': {
                'id':'1',
                'type':'Science'
            }
        })
        data = json.loads(res.data)
        # status code
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertIsInstance(data['question'],dict)

    # testing quizzes with category with all the previous questions
    def test_quizzes_with_category_with_all_previous_questions(self):
        res = self.client().post('quizzes', json= {
            'previous_questions':[20,21,22],
            'quiz_category': {
                'id':'1',
                'type':'Science'
            }
        })
        data = json.loads(res.data)
        # status code
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()