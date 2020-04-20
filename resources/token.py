from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager,
    jwt_refresh_token_required, 
    get_jwt_identity, 
    create_access_token
)


jwt = JWTManager()

_invalid_jti = set()


def mark_jwt_as_invalid(jti):
    _invalid_jti.add(jti)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    return {'is_admin': identity == 1}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'message': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'Token is invalid', 'error': error}), 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({'message': 'User is not authorized to perform the request', 'error': error}), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({'message': 'Fresh token required'}), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'message': 'Provided token has been revoked'}), 401

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in _invalid_jti


class TokenRefreshResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        new_token = create_access_token(identity=get_jwt_identity(), fresh=False)
        return {'access_token': new_token}, 200
