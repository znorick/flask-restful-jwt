import sqlite3
from utils import initializable
from db import db


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def __init__(self, username, password):
        self.id = None
        self.username = username
        self.password = password

    def __str__(self):
        return f'User(id={self.id}, username={self.username}, password=***)'

    def dict_repr(self):
        return {'id': self.id, 'username': self.username}


@initializable
class UserRepository:

    @staticmethod
    def init():
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        #connection.close()
        print('User Repository has been initialized')

    @classmethod
    def find_by_username(cls, username):
        return db.session.query(User).filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return db.session.query(User).filter_by(id=id).first()

    @classmethod
    def save(cls, user):
        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete(cls, user):
        db.session.delete(user)
        db.session.commit()
