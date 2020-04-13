from flask_restful import Resource, reqparse
from models.user import User, UserRepository


class UserResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        rq_data = UserResource.parser.parse_args()
        if UserRepository.find_by_username(rq_data['username']):
            return {'message': f'User {rq_data["username"]} already exists.'}, 400
        user = User(**rq_data)
        UserRepository.save(user)
        return {'message': f'User {user.username} created.'}, 201
