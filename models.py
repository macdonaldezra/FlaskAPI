from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    email = Column(String(150), unique=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    password = Column(String(128))

    @staticmethod
    def set_password(password):
        hasher = PasswordHasher()
        return hasher.hash(password)

    def verify_password(self, password):
        try:
            hasher = PasswordHasher()
            hasher.verify(self.password, password)
            return True
        except VerifyMismatchError:
            return False

    def __repr__(self):
        return ('<User {} {}>'.format(self.first_name, self.last_name))
