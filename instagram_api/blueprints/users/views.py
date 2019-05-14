from flask import Blueprint, jsonify
from flask_jwt import JWT, jwt_required
from models.user import User

users_api_blueprint = Blueprint('users_api',
                                __name__,
                                template_folder='templates')


@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "USERS API"


@users_api_blueprint.route('/<username>', methods=['GET'])
@jwt_required
def show(username):
    user = User.get_or_none(User.username == username)

    if not user:
        resp = {
            'message': 'No user found with this username',
            'ok': False
        }
        # use jsonify to return a response in a JSON format
        return jsonify(resp)

    resp = {
        'message': 'Found user with this username',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,

        },
        'okay': True
    }

    return jsonify(resp)
