import sys
import unittest

from werkzeug.http import parse_cookie
from run import create_app
from models import db, User, Client, Project

def addTestUsers():
    """Add users for managing clients."""
    user1 = User(username='test_user1', email='robmc@gmail.com', first_name='Robert', last_name='Mcd', password='password1')
    user2 = User(username='test_user2', email='johnmc@gmail.com', first_name='John', last_name='Mcd', password='password2')
    test_users = [user1, user2]
    for user in test_users:
        try:
            user.add()
        except:
            pass

def removeTestUsers():
    """Remove users if they are found in the database."""
    ruser1 = User.query.filter_by(username='test_user1').first()
    ruser2 = User.query.filter_by(username='test_user2').first()
    if ruser1:
        db.session.delete(ruser1)
        db.session.commit()
    if ruser2:
        db.session.delete(ruser2)
        db.session.commit()
    db.session.close()

def addTestClients():
    """Add clients for testing."""
    user1 = User.query.filter_by(username='test_user1').first()
    user2 = User.query.filter_by(username='test_user2').first()
    client1 = Client(email='miscemail1@live.com', name='miscclient1', description='misc users files.', user=user1)
    client2 = Client(email='miscemail2@live.com', name='miscclient2', description='misc users files.', user=user1)
    client3 = Client(email='miscemail3@live.com', name='miscclient3', description='misc users files.', user=user1)
    client4 = Client(email='miscemail3@live.com', name='miscclient1', description='misc users files.', user=user2)
    client5 = Client(email='miscemail5@live.com', name='miscclient2', description='misc users files.', user=user2)
    client6 = Client(email='miscemail7@live.com', name='miscclient3', description='misc users files.', user=user2)
    test_clients = [client1, client2, client3, client4, client5, client6]
    for client in test_clients:
        try:
            db.session.add(client)
            db.session.commit()
        except:
            pass

def removeTestClients():
    """Remove clients if they are found in the database."""
    client1 = Client.query.filter_by(email='miscemail1@live.com', name='miscclient1').first()
    client2 = Client.query.filter_by(email='miscemail2@live.com', name='miscclient2').first()
    client3 = Client.query.filter_by(email='miscemail3@live.com', name='miscclient3').first()
    client4 = Client.query.filter_by(email='miscemail3@live.com', name='miscclient1').first()
    client5 = Client.query.filter_by(email='miscemail5@live.com', name='miscclient2').first()
    client6 = Client.query.filter_by(email='miscemail7@live.com', name='miscclient3').first()
    test_clients = [client1, client2, client3, client4, client5, client6]
    for client in test_clients:
        try:
            db.session.delete(client)
            db.session.commit()
        except:
            pass
        db.session.close()

def addTestProjects():
    """Add projects for testing."""
    user1 = User.query.filter_by(username='test_user1').first()
    client = Client.query.with_parent(user1).filter_by(name='miscclient1', email='miscemail1@live.com').first()
    project1 = Project(name='project1', description='project1 description', client=client)
    project2 = Project(name='project2', description='project2 description', client=client)
    project3 = Project(name='project3', description='project3 description', client=client)
    test_projects = [project1, project2, project3]
    for project in test_projects:
        try:
            db.session.add(project)
            db.session.commit()
        except:
            pass

def removeTestProjects():
    """Remove test projects if they are found in the database."""
    project1 = Project.query.filter_by(name='project1').first()
    project2 = Project.query.filter_by(name='project2').first()
    project3 = Project.query.filter_by(name='project3').first()
    test_projects = [project1, project2, project3]
    for project in test_projects:
        try:
            db.session.delete(project)
            db.session.commit()
        except:
            pass
        db.session.close()


class ClientTestCase(unittest.TestCase):
    """Class for main module client test cases."""
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
            addTestClients()
            addTestProjects()

    def testAddClient(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()

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
        json_data = re.get_json()

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
        json_data = re.get_json()

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
        json_data = re.get_json()

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
        json_data = re.get_json()

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.get('/clients')
            self.assertEqual(r.status_code, 201)

    def testGetClientsWithInvalidClientName(self):
        re = self.client().post('/', json={'username': 'test_user1', 
                                                'password': 'password1'})
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.get('/client', json={'client_name': 'miscclient2', 'client_email': 'miscemail1@gmail.com'})
            self.assertEqual(r.status_code, 422)

    def testGetClient(self):
        re = self.client().post('/', json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.get('/client', json={'client_name': 'miscclient1', 'client_email': 'miscemail3@live.com'})
            self.assertEqual(r.status_code, 201)

    def testUpdateClient(self):
        re = self.client().post('/', json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()

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
        json_data = re.get_json()

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
        json_data = re.get_json()

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.delete('/client', json={'client_name': 'miscclient3', 'client_email': 'miscemail7@live.com'})
            self.assertEqual(r.status_code, 308)

    def testCreateProject(self):
        re = self.client().post('/', json={'username': 'test_user2', 
                                                'password': 'password2'})
        self.assertEqual(re.status_code, 201)
        json_data = re.get_json()

        cookie = parse_cookie(re.headers['Set-Cookie'])
        with self.client() as tc:
            tc.set_cookie('127.0.0.1', 'session', str(cookie['session']), path='/', domain='127.0.0.1')
            r = tc.post('/client', json={'client_name': 'miscemail5@live.com', 'project_name': 'miscclient2'})
            self.assertEqual(r.status_code, 202)
            json_data = r.get_json()
            print(json_data)

    def tearDown(self):
        removeTestProjects()
        removeTestClients()
        removeTestUsers()
        db.session.remove()
        self.app_context.pop()