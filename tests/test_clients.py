import sys
import unittest

from werkzeug.http import parse_cookie
from run import create_app
from models import db, User, Client, Project
from .client_helpers import (
                        addTestUsers,
                        removeTestUsers,
                        addTestClients,
                        removeTestClients,
                        addTestProjects,
                        removeTestProjects
                    )



class ClientTestCase(unittest.TestCase):
    """Class for main module client test cases."""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app.app_context():
            db.session.close()
            db.create_all()
            addTestUsers()
            addTestClients()
            addTestProjects()

    def testAddClient(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.post('/clients', json={'name': 'new_client1', 
                                        'email': 'new_client1@live.ca', 'description': 'this is a new client.'})
            self.assertEqual(r.status_code, 201)

    def testInvalidClientName(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.post('/clients', json={'name': 'new_$%client1', 
                                        'email': 'new_client1@live.ca', 'description': 'this is a new client.'})
            self.assertEqual(r.status_code, 422)

    def testTwiceEnteredClient(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.post('/clients', json={'name': 'miscclient1', 'email': 'miscemail1@live.com', 
                                            'description': 'this is a new client.'})
            self.assertEqual(r.status_code, 422)

    def testInvalidClientDescription(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.post('/clients', json={'name': 'miscclient2', 
                                        'email': 'miscemail1@gmail.com', 'description': 't'})
            self.assertEqual(r.status_code, 422)

    def testGetClients(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.get('/clients')
            self.assertEqual(r.status_code, 201)

    def testGetClientsWithInvalidClientName(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.get('/client', json={'client_name': 'miscclient2', 'client_email': 'miscemail1@gmail.com'})
            self.assertEqual(r.status_code, 422)

    def testGetClient(self):
        re = self.client().post('/', json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.get('/client', json={'client_name': 'miscclient1', 'client_email': 'miscemail3@live.com'})
            self.assertEqual(r.status_code, 201)

    def testUpdateClient(self):
        re = self.client().post('/', json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.put('/client', json={'client_email': 'miscemail5@live.com', 'client_name': 'miscclient2', 
                                    'description': 'this is updated.'})
            self.assertEqual(r.status_code, 202)
            json_data = r.get_json()
            self.assertEqual(json_data['description'], 'this is updated.')

    def testUpdateClientWithInvalidName(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.put('/client', json={'client_email': 'miscemail3@live.com', 'client_name': 'miscclient3', 
                                    'name': 'asd@#dsd'})
            self.assertEqual(r.status_code, 422)

    def testDeleteClient(self):
        re = self.client().post('/', json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.delete('/client', json={'client_name': 'miscclient3', 'client_email': 'miscemail7@live.com'})
            self.assertEqual(r.status_code, 308)

    def tearDown(self):
        removeTestProjects()
        removeTestClients()
        removeTestUsers()
        db.session.remove()
        self.app_context.pop()