import json
import sys
import unittest

from werkzeug.http import parse_cookie
from run import create_app
from models import db, User, Client

def addTestUsers():
    """Add users for login, registration, and update testing."""
    user1 = User(username='robmcd3', email='robmc@gmail.com', first_name='Robert', last_name='Mcd', password='Passin123')
    user2 = User(username='johnmc3s', email='johnmc@gmail.com', first_name='John', last_name='Mcd', password='Newpass')
    user3 = User(username='mhird23', email='matt_hird@gmail.com', first_name='Matt', last_name='Hird', password='Passin123')
    user4 = User(username='macdonej24', email='macdonaldezra@gmail.com', first_name='Ezra', last_name='James', password='NewPass123')
    user5 = User(username='andrelineker3', email='andre@telus.net', first_name='Andre', last_name='Lineker', password='Pass241')
    temp_users = [user1, user2, user3, user4, user5]
    for user in temp_users:
        try:
            user.add()
        except:
            pass

def removeTestUsers():
    """Remove users if they are found in the database."""
    ruser1 = User.query.filter_by(email='macdonaldezra@gmail.com').first()
    ruser2 = User.query.filter_by(email='matt_hird@gmail.com').first()
    ruser3 = User.query.filter_by(email='johnmac@gmail.com').first()
    if ruser1:
        db.session.delete(ruser1)
        db.session.commit()
    if ruser2:
        db.session.delete(ruser2)
        db.session.commit()
    if ruser3:
        db.session.delete(ruser3)
        db.session.commit()
    db.session.close()


class MainUserTestCase(unittest.TestCase):
    """Class for main module user test cases."""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()
            addTestUsers()

    def testValidRegistration(self):
        re = self.client().post('/register', json={'username': 'macdonejhlk', 'email': 'macdonaldezra@gmail.com',
                                                   'first_name': 'Ezra', 'last_name': 'James',
                                                   'password': 'NewPass23'})
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()
        vars = json.loads(json_data)
        self.assertEqual(vars['username'], 'macdonejhlk')


    def testInvalidFirstNameRegistration(self):
        re = self.client().post('/register', json={'username': 'madssdf2323', 'email': 'magicman@hotmail.com',
                                                   'first_name': 'B', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['first_name'])

    def testInvalidEmailRegistration(self):
        re = self.client().post('/register', json={'username': '1mm23md0e', 'email': 'newmail@gmail',
                                                   'first_name': 'Brendan', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['email'])

    def testInvalidNameRegistration(self):
        re = self.client().post('/register', json={'username': '1mm23md0e', 'email': 'newmail@gmail.com',
                                                   'first_name': 'Bre$#ndan', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['first_name'])

    def testInvalidPasswordRegistration(self):
        re = self.client().post('/register', json={'username': 'mynameis3', 'email': 'newmail2@gmail.com',
                                                   'first_name': 'Brendan', 'last_name': 'Macklin',
                                                   'password': 'p%$#sdfsds'})
        json_data = re.get_json()
        self.assertEqual(re.status_code, 422)
        self.assertIsNotNone(json_data['errors']['password'])

    def testInvalidUsernameRegistration(self):
        re = self.client().post('/register', json={'username': 'fd%$a%@sdf', 'email': 'newmail3@gmail.com',
                                                   'first_name': 'Brend23an', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testInvalidNoUsernameRegistration(self):
        re = self.client().post('/register', json={'username': '', 'email': 'newmail2@gmail.com',
                                                   'first_name': 'Brendan', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors']['username'])

    def testProperLogin(self):
        re = self.client().post('/', json={'username': 'mhird23', 
                                                'password': 'Passin123'})
        json_data = re.get_json()
        self.assertEqual(re.status_code, 201)
        
    def testLoginInvalidUsername(self):
        re = self.client().post('/', json={'username': 'macdonej', 
                                                'password': 'NewPass23'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()        
        self.assertIsNotNone(json_data['errors'])

    def testLoginInvalidPassword(self):
        re = self.client().post('/', json={'username': 'macdonej24', 
                                                'password': 'NewPass21'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testUpdateFirstName(self):
        resp = self.client().post('/', json={'username': 'robmcd3', 
                                        'password': 'Passin123'})
        self.assertEqual(resp.status_code, 201)
        cookie = parse_cookie(resp.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.put('/profile', json={'user': {'first_name': 'Robin'}})
            self.assertEqual(r.status_code, 202)
            json_data = r.get_json()
            self.assertEqual(json_data['first_name'], 'Robin')

    def testUpdatePassword(self):
        resp = self.client().post('/', json={'username': 'robmcd3', 
                                        'password': 'Passin123'})
        self.assertEqual(resp.status_code, 201)
        cookie = parse_cookie(resp.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.put('/profile', json={'new_password': 'NewPass21', 'user': {'password': 'Passin123'}})
            self.assertEqual(r.status_code, 202)

    def testBadUpdatePassword(self):
        re = self.client().post('/', json={'username': 'macdonej24', 
                                                'password': 'NewPass123'})
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.put('/profile', json={'new_password': 'NEsd23d', 'user': {'password': 'sdfssdsd'}})
            self.assertEqual(r.status_code, 422)
            json_data = r.get_json()
            self.assertIsNotNone(json_data['errors'])

    def testDeleteUser(self):
        resp = self.client().post('/', json={'username': 'andrelineker3', 'password': 'Pass241'})
        self.assertEqual(resp.status_code, 201)
        json_data = resp.get_json()
        cookie = parse_cookie(resp.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.delete('/profile', json={'confirm_password': 'Pass241'})
            json_data = r.get_json()
            self.assertEqual(r.status_code, 308)

    def tearDown(self):
        removeTestUsers()
        db.session.remove()
        self.app_context.pop()
