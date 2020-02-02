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
