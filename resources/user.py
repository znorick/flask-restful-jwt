from flask_restful import Resource, reqparse
from models.user import User, UserRepository
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_claims,
    get_raw_jwt
)
from .token import mark_jwt_as_invalid


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


class UserLoginResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    @classmethod
    def post(cls):
        rq_data = cls.parser.parse_args()
        user = UserRepository.find_by_username(rq_data['username'])
        if user and safe_str_cmp(rq_data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogoutResource(Resource):

    @jwt_required
    def post(self):
        mark_jwt_as_invalid(get_raw_jwt()['jti'])
        return {'message': 'Logged out'}, 200


class UserResource(Resource):

    def get(self, user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'message': f'User with ID {user_id} was not found'}, 404
        return user.dict_repr(), 200

    @jwt_required
    def delete(self, user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin priviledge reqired'}, 401
        user = UserRepository.find_by_id(user_id)
        if not user:
            return {'message': f'User with ID {user_id} was not found'}, 404
        UserRepository.delete(user)
        return {'message': f'User with ID {user_id} deleted'}, 200
