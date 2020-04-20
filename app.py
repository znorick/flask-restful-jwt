import os
from flask import Flask, jsonify
from flask_restful import Api
from resources.item import ItemResource, ItemListResource
from resources.user import (
    UserRegisterResource, 
    UserLoginResource, 
    UserLogoutResource,
    UserResource
)
from resources.store import StoreResource
from resources.token import jwt, TokenRefreshResource
from datetime import timedelta
from db import db


app = Flask(__name__)
app.secret_key = 'some_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt.init_app(app)

api = Api(app)
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemListResource, '/items')
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserLogoutResource, '/logout')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(StoreResource, '/store/<string:name>')
api.add_resource(TokenRefreshResource, '/refresh')


# Comment this to run at Heroku
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
