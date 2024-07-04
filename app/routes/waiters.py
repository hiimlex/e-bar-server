from flask import Blueprint, request, jsonify
from ..models import Waiters
from .. import db

bp = Blueprint('waiters', __name__, url_prefix='/garcons')

@bp.route('', methods=['GET'])
def get_waiters():
    filters = request.args
    query = Waiters.query
    
    # if 'ordem' in filters:
    #     if filters['ordem'] == 'nome':
    #         query = query.order_by(Waiters.name)

    waiters = query.all()
    return jsonify([waiter.as_dict() for waiter in waiters])

@bp.route('', methods=['POST'])
def create_waiter():
    data = request.get_json()
    new_waiter = Waiters(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        password=data['password'],
        active=data.get('active', True)
    )
    db.session.add(new_waiter)
    db.session.commit()
    return jsonify(new_waiter.as_dict()), 201

@bp.route('/<int:waiter_id>', methods=['PUT'])
def update_waiter(waiter_id):
    data = request.get_json()
    waiter = Waiters.query.get_or_404(waiter_id)
    waiter.name = data.get('name', waiter.name)
    waiter.email = data.get('email', waiter.email)
    waiter.phone = data.get('phone', waiter.phone)
    waiter.password = data.get('password', waiter.password)
    waiter.active = data.get('active', waiter.active)
    db.session.commit()
    return jsonify(waiter.as_dict())

@bp.route('/<int:waiter_id>', methods=['DELETE'])
def delete_waiter(waiter_id):
    waiter = Waiters.query.get_or_404(waiter_id)
    db.session.delete(waiter)
    db.session.commit()
    return '', 204
