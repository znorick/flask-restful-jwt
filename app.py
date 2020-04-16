import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.item import ItemResource, ItemListResource
from resources.user import UserRegisterResource, UserResource
from resources.store import StoreResource
from datetime import timedelta
from db import db


app = Flask(__name__)
app.secret_key = 'some_key'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'username' # default
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWT(app, authenticate, identity) # default /auth
api = Api(app)
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemListResource, '/items')
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(StoreResource, '/store/<string:name>')

# Comment this to run at Heroku
@app.before_first_request
def create_tables():
    db.create_all()

@jwt.auth_response_handler
def auth_resoponse_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

@jwt.jwt_error_handler
def jwt_error_handler(error):
    return jsonify({
        'message': error.description,
        'error': error.error
    }), error.status_code

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
