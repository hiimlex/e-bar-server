from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import asc, desc, func

from ..utils.socket import socket_update_orders
from ..models import OrderProducts, Orders, Products,Waiters, Tables
from .. import db


bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('', methods=['GET'])
@jwt_required()
def get_all_orders():
    filters = request.args
    
    query = db.session.query(
        Orders.id,
        Orders.waiter_id,
        Orders.customers,
        Orders.table_id,
        Orders.total,
        Orders.payment_method,  
        Orders.status,
        Orders.finalized_at,
        Orders.created_at,
        Orders.updated_at,
        Waiters.name.label('waiter_name'),
        func.sum(Products.price * OrderProducts.quantity + Products.price * OrderProducts.delivered).label('total'),
    ).join(Waiters
    ).group_by(Orders.id
    ).outerjoin(OrderProducts, Orders.id == OrderProducts.order_id
    ).outerjoin(Products, OrderProducts.product_id == Products.id
    )
    
    if ('status' in filters):
        query = query.filter(Orders.status == filters['status'])
    
    if('order_id' in filters):
        query = query.filter(Orders.id == filters['order_id'])

    if('waiter_id' in filters):
        query = query.filter(Orders.waiter_id == filters['waiter_id'])

    if('sort_by' in filters):
        if('sort_order' in filters):
            if(filters['sort_order'] == 'asc'):
                query = query.order_by(asc(filters['sort_by']))
            else:
                query = query.order_by(desc(filters['sort_by']))

    orders = query.all()

    orders_list = []
    for order in orders:
        order_products_query = db.session.query(
            OrderProducts.id.label('order_product_id'),
            OrderProducts.product_id,
            OrderProducts.quantity,
            Products.name,
            Products.image_url,
            Products.price,
            OrderProducts.status,
            Products.stock,
            OrderProducts.delivered
        ).join(Products
        ).filter(OrderProducts.order_id == order.id)

        if ('product_status' in filters):
            order_products_query = order_products_query.filter(OrderProducts.status == filters['product_status'])                                          

        order_products = order_products_query.order_by(asc(OrderProducts.status)).group_by(OrderProducts.id).all()

        order_products_list = []
        for product in order_products:
            product_dict = {
                'order_product_id': product.order_product_id,
                'product_id': product.product_id,
                'name': product.name,
                'image_url': product.image_url,
                'price': float(product.price),
                'quantity': product.quantity,
                'status': product.status,
                'stock': product.stock,
                'delivered': product.delivered
            }
            order_products_list.append(product_dict)

   
        order_dict = {
            'id': order.id,
            'waiter_id': order.waiter_id,
            'waiter_name': order.waiter_name,
            'table_id': order.table_id,
            'total': float(order.total) if order.total else 0,
            'payment_method': order.payment_method,
            'status': order.status,
            'finalized_at': order.finalized_at,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'products': order_products_list,
            'customers': order.customers
        }

        orders_list.append(order_dict)

    return jsonify(orders_list)

@bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    waiter_id = get_jwt_identity()
    waiter = Waiters.query.get(waiter_id)

    table = Tables.query.filter(Tables.id == data['table_id']).first()

    if(table is None):
        return jsonify({'error': 'Table not found'}), 404
    

    if table.in_use:
        return jsonify({'error': 'Table already in use'}), 400

    new_order = Orders(
        waiter_id=waiter.id,
        table_id=table.id,
        status = 'on_demand',
        customers = data['customers']
    )
    table.in_use = True
    table.waiter_id = waiter.id
    table.order_id = new_order.id
    
    db.session.add(new_order)
    db.session.commit()
    
    socket_update_orders()
    
    return jsonify(new_order.as_dict()), 201

@bp.route('/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    data = request.get_json()
    order = Orders.query.get_or_404(order_id)
    order.payment_method = data.get('payment_method', order.payment_method)
    order.status = data.get('status', order.status)
    order.finalized_at = data.get('finalized_at', order.finalized_at)
    
    db.session.commit()
    
    socket_update_orders()
    
    return jsonify(order.as_dict())

@bp.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = Orders.query.get_or_404(order_id)

    table = Tables.query.filter(Tables.id == order.table_id).first()
    table.in_use = False

    db.session.delete(order)
    db.session.commit()
    
    socket_update_orders()
    return '', 204

