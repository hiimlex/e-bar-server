from flask import Blueprint, request, jsonify
from ..models import Order
from .. import db

bp = Blueprint('orders', __name__, url_prefix='/pedidos')

@bp.route('', methods=['GET'])
def get_orders():
    filters = request.args
    query = Order.query
    
    if 'status' in filters:
        query = query.filter_by(status=filters['status'])
    
    if 'garcom' in filters:
        query = query.filter(Order.waiter.has(name=filters['garcom']))
    
    if 'ordem' in filters:
        if filters['ordem'] == 'mesa':
            query = query.order_by(Order.table_id)
    
    orders = query.all()
    return jsonify([order.to_dict() for order in orders])

@bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        waiter_id=data['waiter_id'],
        table_id=data['table_id'],
        products=data['products'],
        total=data['total'],
        payment_method=data['payment_method'],
        status=data['status']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    order.waiter_id = data.get('waiter_id', order.waiter_id)
    order.table_id = data.get('table_id', order.table_id)
    order.products = data.get('products', order.products)
    order.total = data.get('total', order.total)
    order.payment_method = data.get('payment_method', order.payment_method)
    order.status = data.get('status', order.status)
    order.finalized_at = data.get('finalized_at', order.finalized_at)
    db.session.commit()
    return jsonify(order.to_dict())

@bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return '', 204
