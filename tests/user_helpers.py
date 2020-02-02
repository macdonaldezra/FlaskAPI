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
    ruser1 = User.query.filter_by(email='macdonaldezra@gmail.com').first()
    ruser2 = User.query.filter_by(email='matt_hird@gmail.com').first()
    ruser3 = User.query.filter_by(email='johnmac@gmail.com').first()
    ruser4 = User.query.filter_by(email='robmc@gmail.com').first()
    ruser5 = User.query.filter_by(email='andre@telus.net').first()
    temp_users = [ruser1, ruser2, ruser3, ruser4, ruser5]
    for user in temp_users:
        if user:
            db.session.delete(user)
            db.session.commit()
    db.session.close()

def DropAllTables(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn=db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in 
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()