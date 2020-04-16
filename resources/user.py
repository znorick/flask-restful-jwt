from flask_restful import Resource, reqparse
from models.user import User, UserRepository


class UserRegisterResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        rq_data = UserRegisterResource.parser.parse_args()
        if UserRepository.find_by_username(rq_data['username']):
            return {'message': f'User {rq_data["username"]} already exists.'}, 400
        user = User(**rq_data)
        UserRepository.save(user)
        return {'message': f'User {user.username} created with ID {user.id}.'}, 201


class UserResource(Resource):

    def get(self, user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'message': f'User with ID {user_id} was not found'}, 404
        return user.dict_repr(), 200

    def delete(self, user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'message': f'User with ID {user_id} was not found'}, 404
        UserRepository.delete(user)
        return {'message': f'User with ID {user_id} deleted'}, 200
