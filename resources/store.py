from flask_restful import Resource
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from models.store import Store


class StoreResource(Resource):

    @jwt_optional
    def get(self, name):
        store = Store.find_by_name(name)
        if store:
            if get_jwt_identity():
                return store.dict_repr(), 200
            return {'name': name, 
                    'items': [item.name for item in store.items],
                    'message': 'Price data is available after you log in'}, 200
        return {'message': f'Store {name} not found.'}, 404

    @jwt_required
    def post(self, name):
        if Store.find_by_name(name):
            return {'message': f'Store {name} already exists.'}, 400
        store = Store(name)
        store.save()
        return store.dict_repr(), 201
