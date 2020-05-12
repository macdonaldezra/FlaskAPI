from models import db, User, Client, Project


def removeTestEntries():
    db.session.query(Project).delete()
    db.session.query(Client).delete()
    db.session.query(User).delete()
    db.session.commit()
    db.session.close()


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

