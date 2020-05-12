from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
        MetaData,
        Table,
        DropTable,
        ForeignKeyConstraint,
        DropConstraint,
        )

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
    db.session.query(User).delete()
    db.session.commit()
    db.session.close()

