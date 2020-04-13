from resources.user import UserRepository
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = UserRepository.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserRepository.find_by_id(user_id)
