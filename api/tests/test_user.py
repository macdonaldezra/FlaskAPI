import os
import json
import sys
import unittest

from werkzeug.http import parse_cookie

from run import create_app
from settings import routes
from models import db, User, Client
from .user_helpers import (
                            addTestUsers,
                            removeTestUsers
                          )


DOMAIN = '127.0.0.1'

class MainUserTestCase(unittest.TestCase):
    """Class for main module user test cases."""

    @classmethod
    def setUpClass(cls):
        os.environ['FLASK_ENV'] = 'testing'
        cls.app = create_app()
        cls.client = cls.app.test_client
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        with cls.app.app_context():
            db.create_all()
            addTestUsers()

    @classmethod
    def tearDownClass(cls):
        removeTestUsers()
        db.session.remove()
        cls.app_context.pop()

    def get_cookie(self, username: str, password: str):
        resp = self.client().post(routes.LOGIN, json={'username': username, 'password': password})
        cookie = parse_cookie(resp.headers['Set-Cookie'])
        return cookie


    def testValidRegistration(self):
        re = self.client().post(routes.REGISTRATION, json={'username': 'macdonejhlk', 
                                                   'email': 'macdonaldezra@gmail.com',
                                                   'first_name': 'Ezra',
                                                   'last_name': 'James',
                                                   'password': 'NewPass23'
                                                   })
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()
        self.assertEqual(json_data['username'], 'macdonejhlk')


    def testInvalidFirstNameRegistration(self):
        re = self.client().post(routes.REGISTRATION, json={'username': 'madssdf2323',
                                                    'email': 'magicman@hotmail.com',
                                                    'first_name': 'B', 
                                                    'last_name': 'Macklin',
                                                    'password': 'passwords'
                                                   })
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['first_name'])


    def testInvalidEmailRegistration(self):
        re = self.client().post(routes.REGISTRATION, json={'username': '1mm23md0e', 
                                                    'email': 'newmail@gmail',
                                                    'first_name': 'Brendan', 
                                                    'last_name': 'Macklin',
                                                    'password': 'passwords'
                                                   })
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['email'])


    def testInvalidNameRegistration(self):
        re = self.client().post(routes.REGISTRATION, json={'username': '1mm23md0e', 
                                                    'email': 'newmail@gmail.com',
                                                    'first_name': 'Bre$#ndan', 
                                                    'last_name': 'Macklin',
                                                    'password': 'passwords'
                                                   })
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['first_name'])


    def testInvalidPasswordRegistration(self):
        re = self.client().post(routes.REGISTRATION, json={'username': 'mynameis3', 
                                                    'email': 'newmail2@gmail.com',
                                                    'first_name': 'Brendan', 
                                                    'last_name': 'Macklin',
                                                    'password': 'p%$#sdfsds'
                                                   })
        json_data = re.get_json()
        self.assertEqual(re.status_code, 422)
        self.assertIsNotNone(json_data['errors']['password'])


    def testInvalidUsernameRegistration(self):
        re = self.client().post(routes.REGISTRATION, json={'username': 'fd%$a%@sdf', 
                                                    'email': 'newmail3@gmail.com',
                                                    'first_name': 'Brend23an', 
                                                    'last_name': 'Macklin',
                                                    'password': 'passwords'
                                                    })
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['username'])


    def testInvalidNoUsernameRegistration(self):
        re = self.client().post(routes.REGISTRATION, json={'username': '', 
                                                    'email': 'newmail2@gmail.com',
                                                    'first_name': 'Brendan', 
                                                    'last_name': 'Macklin',
                                                    'password': 'passwords'
                                                    })
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['username'])


    def testProperLogin(self):
        re = self.client().post(routes.LOGIN, json={'username': 'mhird23', 
                                           'password': 'Passin123'
                                           })
        self.assertEqual(re.status_code, 201)


    def testLoginInvalidUsername(self):
        re = self.client().post(routes.LOGIN, json={'username': 'macdonej', 
                                           'password': 'NewPass23'
                                           })
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()        
        self.assertIsNotNone(json_data['errors'])


    def testLoginInvalidPassword(self):
        re = self.client().post(routes.LOGIN, json={'username': 'macdonej24', 
                                           'password': 'NewPass21'
                                           })
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])


    def testUpdateFirstName(self):
        cookie = self.get_cookie('mhird23', 'Passin123')
        with self.client() as client:
            client.set_cookie(DOMAIN, 'session', str(cookie['session']), 
                              path=routes.LOGIN, domain=DOMAIN)
            r = client.put(routes.PROFILE, json={'user': {'first_name': 'Robin'}})
            self.assertEqual(r.status_code, 202)
            json_data = r.get_json()
            self.assertEqual(json_data['first_name'], 'Robin')


    def testUpdatePassword(self):
        cookie = self.get_cookie('robmcd3', 'Passin123')
        with self.client() as client:
            client.set_cookie(DOMAIN, 'session', str(cookie['session']), 
                              path=routes.LOGIN, domain=DOMAIN)
            r = client.put(routes.PROFILE, json={'new_password': 'NewPass21', 'user': {'password': 'Passin123'}})
            self.assertEqual(r.status_code, 202)


    def testBadUpdatePassword(self):
        cookie = self.get_cookie('macdonej24', 'NewPass123')
        with self.client() as client:
            client.set_cookie(DOMAIN, 'session', str(cookie['session']), 
                              path=routes.LOGIN, domain=DOMAIN)
            r = client.put(routes.PROFILE, json={'new_password': 'NEsd23d', 'user': {'password': 'sdfssdsd'}})
            self.assertEqual(r.status_code, 422)
            json_data = r.get_json()
            self.assertIsNotNone(json_data['errors'])


    def testDeleteUser(self):
        cookie = self.get_cookie('andrelineker3', 'Pass241')
        with self.client() as client:
            client.set_cookie(DOMAIN, 'session', str(cookie['session']), 
                              path=routes.LOGIN, domain=DOMAIN)
            r = client.delete(routes.PROFILE, json={'confirm_password': 'Pass241'})
            self.assertEqual(r.status_code, 308)
