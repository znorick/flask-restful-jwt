from db import db


class Store(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    items = db.relationship('Item')

    def __init__(self, name):
        self.name = name

    def dict_repr(self):
        return {'id': self.id, 'name': self.name, 'items': [item.dict_repr() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
