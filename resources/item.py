from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import Item, ItemRepository


class ItemResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Cannot be blank.')
    parser.add_argument('store_id', type=int, required=True, help='Cannot be blank.')

    def get(self, name):
        item = ItemRepository.find_by_name(name)
        return (item.dict_repr(), 200) if item else ({'message': f"Item '{name}' not found."}, 404)

    @jwt_required()
    def post(self, name):
        print(f'{current_identity.username} is trying to create an item "{name}".')
        if ItemRepository.find_by_name(name):
            return {'message': f"Item '{name}' already exists."}, 400
        rq_data = ItemResource.parser.parse_args()
        item = Item(name, **rq_data)
        ItemRepository.save(item)
        return item.dict_repr(), 201

    @jwt_required()
    def put(self, name):
        print(f'{current_identity.username} is trying to update an item "{name}".')
        rq_data = ItemResource.parser.parse_args()
        item = ItemRepository.find_by_name(name)
        if not item:
            item = Item(name, **rq_data)
        else:
            item.price = rq_data['price']
        ItemRepository.save(item)
        return item.dict_repr()

    @jwt_required()
    def delete(self, name):
        print(f'{current_identity.username} is trying to delete an item "{name}".')
        item = ItemRepository.find_by_name(name)
        if not item:
            return {'message': f"Item '{name}' does not exist."}, 400
        ItemRepository.delete(item)
        return {'message': f"Item '{name}' has been deleted."}

class ItemListResource(Resource):
    def get(self):
        items = ItemRepository.get_all()
        if items:
            # list(map(lambda item: item.dict_repr(), items))
            return {'items': [item.dict_repr() for item in items]}, 200
        else:
            return {'message': 'No items found.'}, 404
