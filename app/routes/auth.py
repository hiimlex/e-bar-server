from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import Waiters
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    waiter = Waiters.query.filter_by(email=data['email']).first()
    
    if waiter and check_password_hash(waiter.password, data['password']):
        access_token = create_access_token(identity=waiter.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad email or password"}), 401
