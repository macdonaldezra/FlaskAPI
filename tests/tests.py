import os
import unittest

from db import Session
from run import create_app
from models import User


class MainTestCase(unittest.TestCase):
    """Class for main test case."""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def testUserRegistration(self):
        re = self.client().post('/register', json={'email': 'macdonaldezra@gmail.com',
                                                   'first_name': 'Ezra', 'last_name': 'James',
                                                   'password': 'NewPass23'})
        self.assertEqual(re.status_code, 201)
        self.assertEqual(re.headers['Location'], 'http://localhost/home')
        self.assertIsNotNone(re.headers['Authorization'])

    def testShortName(self):
        re = self.client().post('/register', json={'email': 'magicman@hotmail.com',
                                                   'first_name': 'B', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testInvalidEmail(self):
        re = self.client().post('/register', json={'email': 'badnewemail',
                                                   'first_name': 'Brendan', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testProperLogin(self):
        re = self.client().post('/', json={'email': 'matt_hird@gmail.com', 
                                                'password': 'Passin123'})
        self.assertEqual(re.status_code, 201)
        self.assertEqual(re.headers['Location'], 'http://localhost/home')
        self.assertIsNotNone(re.headers['Authorization'])

    def testLoginInvalidEmail(self):
        re = self.client().post('/', json={'email': 'macdonej', 
                                                'password': 'NewPass23'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testLoginInvalidPassword(self):
        re = self.client().post('/', json={'email': 'macdonaldezra@gmail.com', 
                                                'password': 'NewPass21'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testTokenRequired(self):
        headers = {'Authorization': 'kmifqmwef234'}
        re = self.client().get('/home', headers=headers)
        print(re.headers)
        self.assertEqual(re.status_code, 401)
        self.assertEqual(re.headers['Location'], 'http://localhost/home')

    def tearDown(self):
        ruser = Session.query(User).filter_by(email='macdonaldezra@gmail.com').first()
        if ruser:
            Session.delete(ruser)
            Session.commit()
        Session.close()
