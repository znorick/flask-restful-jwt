from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import Store


class StoreResource(Resource):

    def get(self, name):
        store = Store.find_by_name(name)
        if store:
            return store.dict_repr(), 200
        return {'message': f'Store {name} not found.'}, 404

    @jwt_required()
    def post(self, name):
        if Store.find_by_name(name):
            return {'message': f'Store {name} already exists.'}, 400
        store = Store(name)
        store.save()
        return store.dict_repr(), 201
