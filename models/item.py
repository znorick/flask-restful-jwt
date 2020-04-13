import sqlite3
from utils import initializable
from db import db


class Item(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('Store')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def dict_repr(self):
        return {'name': self.name, 'price': self.price}


@initializable
class ItemRepository:

    @staticmethod
    def init():
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
        #cursor.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL)')
        #connection.close()
        print('Item Repository has been initialized')

    @classmethod
    def find_by_name(cls, name):
        return db.session.query(Item).filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        return db.session.query(Item).all()

    @classmethod
    def save(self, item):
        db.session.add(item)
        db.session.commit()

    @classmethod
    def update(cls, item):
        cls.save(item)

    @classmethod
    def delete(cls, item):
        db.session.delete(item)
        db.session.commit()
