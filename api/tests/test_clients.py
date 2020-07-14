import os
import sys
import unittest

from werkzeug.http import parse_cookie

from run import create_app
from settings import routes
from models import db, User, Client, Project
from .client_helpers import (
                        addTestUsers,
                        addTestClients,
                        addTestProjects,
                        removeTestEntries
                    )


DOMAIN = '127.0.0.1'

class ClientTestCase(unittest.TestCase):
    """Class for main module client test cases."""
   
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
            addTestClients()
            addTestProjects()

    @classmethod
    def tearDownClass(cls):
        removeTestEntries()
        db.session.remove()
        cls.app_context.pop()

    def get_cookie(self, username: str, password: str):
        resp = self.client().post(routes.LOGIN, json={'username': username, 'password': password})
        cookie = parse_cookie(resp.headers['Set-Cookie'])
        return cookie


    def testAddClient(self):
        cookie = self.get_cookie('test_user1', 'password1')
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.post(routes.CLIENTS, json={'name': 'new_client1', 
                                              'email': 'new_client1@live.ca', 
                                              'description': 'this is a new client.'
                                              })
            self.assertEqual(r.status_code, 201)


    def testInvalidClientName(self):
        cookie = self.get_cookie('test_user1', 'password1')
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.post(routes.CLIENTS, json={'name': 'new_$%client1', 
                                              'email': 'new_client1@live.ca', 
                                              'description': 'this is a new client.'
                                              })
            self.assertEqual(r.status_code, 422)


    def testTwiceEnteredClient(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.post(routes.CLIENTS, json={'name': 'miscclient1', 
                                              'email': 'miscemail1@live.com', 
                                              'description': 'this is a new client.'
                                              })
            self.assertEqual(r.status_code, 422)


    def testInvalidClientDescription(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.post(routes.CLIENTS, json={'name': 'miscclient2', 
                                              'email': 'miscemail1@gmail.com', 
                                              'description': 't'
                                              })
            self.assertEqual(r.status_code, 422)


    def testGetClients(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.get(routes.CLIENTS)
            self.assertEqual(r.status_code, 201)


    def testGetClientsWithInvalidClientName(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.get(routes.CLIENT, json={'client_name': 'miscclient2', 
                                            'client_email': 'miscemail1@gmail.com'
                                            })
            self.assertEqual(r.status_code, 422)


    def testGetClient(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.get(routes.CLIENT, json={'client_name': 'miscclient1', 
                                            'client_email': 'miscemail3@live.com'
                                            })
            self.assertEqual(r.status_code, 201)


    def testUpdateClient(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.put(routes.CLIENT, json={'client_email': 'miscemail5@live.com', 
                                            'client_name': 'miscclient2', 
                                            'description': 'this is updated.'
                                            })
            self.assertEqual(r.status_code, 202)
            json_data = r.get_json()
            self.assertEqual(json_data['description'], 'this is updated.')


    def testUpdateClientWithInvalidName(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user1', 
                                                    'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.put(routes.CLIENT, json={'client_email': 'miscemail3@live.com', 
                                            'client_name': 'miscclient3', 
                                            'name': 'asd@#dsd'
                                            })
            self.assertEqual(r.status_code, 422)


    def testDeleteClient(self):
        re = self.client().post(routes.LOGIN, json={'username': 'test_user2', 
                                                    'password': 'password2'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), 
                          path=routes.LOGIN, domain='127.0.0.1')
            r = tc.delete(routes.CLIENT, json={'client_name': 'miscclient3', 
                                               'client_email': 'miscemail7@live.com'
                                              })
            self.assertEqual(r.status_code, 308)

