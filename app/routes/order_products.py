from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from ..utils.socket import socket_update_orders
from .. import db

from app.models import OrderProducts, Orders, Products


bp = Blueprint('order_products', __name__, url_prefix='/order-products')

@bp.route('/<int:order_id>/add', methods=['PUT'])
@jwt_required()
def add_products_to_order(order_id):
    data = request.get_json()
    order = Orders.query.get_or_404(order_id)

    if(data['products']):
        for product in data['products']:
            product_id = product['product_id']
            quantity = product['quantity']
            

            query = OrderProducts.query.filter_by(order_id=order.id, product_id=product_id).filter(OrderProducts.status != 'delivered')

            if 'order_product_id' in product:
                query = query.filter_by(id=product['order_product_id'])

            order_product = query.first()

            print(order_product)

            product_ref = Products.query.get(product_id)

            if order_product != None:                
                diff = order_product.quantity - quantity
                product_ref.stock += diff

                order_product.quantity = quantity

                if(quantity == 0 and order_product.delivered == 0):
                    db.session.delete(order_product)

            else:
                order_product = OrderProducts(
                    order_id=order.id,
                    product_id=product_id,
                    quantity=quantity
                )
                product_ref.stock -= quantity
                db.session.add(order_product)

    socket_update_orders()

    db.session.commit()
    return {}, 204

@bp.route('/<int:order_id>/deliver', methods=['POST'])
@jwt_required()
def deliver_products_from_order(order_id):
    data = request.get_json()
    order = Orders.query.get_or_404(order_id)

    op_ids = [op['order_product_id'] for op in data['order_products']]

    order_products = OrderProducts.query.filter(OrderProducts.order_id == order.id
    ).filter(OrderProducts.id.in_(op_ids)
    ).all()

    for op in order_products:
        op.status = 'delivered'
        op.delivered += op.quantity
        op.quantity = 0

    socket_update_orders()

    db.session.commit()
    return {}, 204