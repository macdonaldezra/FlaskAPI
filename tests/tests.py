import os
import unittest

from run import create_app
from models import User, db
from auth import generateToken

def addTestUsers():
    try:
        user1 = User(email='robmc@gmail.com', first_name='Robert', last_name='Mcd', password='Passin123')
        user1.add()
    except:
        pass
    try:
        user2 = User(email='johnmc@gmail.com', first_name='John', last_name='Mcd', password='Newpass')
        user2.add()
    except:
        pass
    try:
        user3 = User(email='matt_hird@gmail.com', first_name='Matt', last_name='Hird', password='Passin123')
        user3.add()
    except:
        pass


def removeTestUsers():
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


class MainTestCase(unittest.TestCase):
    """Class for main test case."""
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

    def testUserRegistration(self):
        re = self.client().post('/register', json={'email': 'macdonaldezra@gmail.com',
                                                   'first_name': 'Ezra', 'last_name': 'James',
                                                   'password': 'NewPass23'})
        self.assertEqual(re.status_code, 201)
        self.assertEqual(re.headers['Location'], 'http://localhost/profile')
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

    def testInvalidPassword(self):
        re = self.client().post('/register', json={'email': 'badnewemail',
                                                   'first_name': 'Brendan', 'last_name': 'Macklin',
                                                   'password': 'passwor%$#@#ds'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testInvalidName(self):
        re = self.client().post('/register', json={'email': 'badnewemail',
                                                   'first_name': 'Brend23an', 'last_name': 'Macklin',
                                                   'password': 'passwords'})
        self.assertEqual(re.status_code, 422)
        json_data = re.get_json()
        self.assertIsNotNone(json_data['errors'])

    def testProperLogin(self):
        re = self.client().post('/', json={'email': 'matt_hird@gmail.com', 
                                                'password': 'Passin123'})
        json_data = re.get_json()
        self.assertEqual(re.status_code, 201)
        self.assertEqual(re.headers['Location'], 'http://localhost/profile')
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
        re = self.client().get('/profile', headers=headers)
        self.assertEqual(re.status_code, 401)
        self.assertEqual(re.headers['Location'], 'http://localhost/profile')

    def testUpdatePassword(self):
        re = self.client().post('/', json={'email': 'robmc@gmail.com', 
                                                'password': 'Passin123'})
        self.assertEqual(re.status_code, 201)
        self.assertEqual(re.headers['Location'], 'http://localhost/profile')
        self.assertIsNotNone(re.headers['Authorization'])

        headers = {'Authorization': re.headers['Authorization']}
        re = self.client().put('/profile', json={'new_password': 'NewPass21', 'user': {'password': 'Passin123'}}, headers=headers)
        self.assertEqual(re.status_code, 202)

    def testUpdateEmail(self):
        re = self.client().post('/', json={'email': 'johnmc@gmail.com', 
                                                'password': 'Newpass'})
        self.assertEqual(re.status_code, 201)
        self.assertEqual(re.headers['Location'], 'http://localhost/profile')
        self.assertIsNotNone(re.headers['Authorization'])
        
        headers = {'Authorization': re.headers['Authorization']}

        re = self.client().put('/profile', json={'user': {'email': 'johnmac@gmail.com'}}, headers=headers)
        json_data = re.get_json()
        self.assertEqual(re.status_code, 202)
        self.assertEqual(json_data['email'], 'johnmac@gmail.com')

    def testBadUpdatePassword(self):
        re = self.client().post('/', json={'email': 'matt_hird@gmail.com', 
                                                'password': 'Passin123'})
        json_data = re.get_json()
        self.assertEqual(re.status_code, 201)
        self.assertEqual(re.headers['Location'], 'http://localhost/profile')
        self.assertIsNotNone(re.headers['Authorization'])

        headers = {'Authorization': re.headers['Authorization']}
        re = self.client().put('/profile', json={'new_password': 'NewPass21', 'user': {'password': 'Passwerw3'}}, headers=headers)
        self.assertEqual(re.status_code, 422)

    def tearDown(self):
        removeTestUsers()
        db.session.remove()
        self.app_context.pop()
