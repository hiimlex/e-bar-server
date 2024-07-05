from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..models import Waiters
from werkzeug.security import check_password_hash

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    waiter = Waiters.query.filter_by(email=data['email']).first()
    
    if waiter and check_password_hash(waiter.password, data['password']):
        access_token = create_access_token(identity=waiter.id)
        response = jsonify(access_token=access_token)
        response.headers.add('Access-Control-Allow-Origin', '*')
        
        return response, 200
    

    return jsonify({"msg": "Bad email or password"}), 401

@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    waiter_id = get_jwt_identity()

    waiter = Waiters.query.get(waiter_id)

    return jsonify(waiter.as_dict()), 200