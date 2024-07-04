from flask import Blueprint, request, jsonify
from ..models import Products
from .. import db

bp = Blueprint('products', __name__, url_prefix='/produtos')

@bp.route('', methods=['GET'])
def get_products():
    filters = request.args
    query = Products.query
    
    # if 'categoria' in filters:
    #     query = query.filter_by(category=filters['categoria'])
    
    # if 'nome' in filters:
    #     query = query.filter(Products.name.like(f"%{filters['nome']}%"))

    # if 'ordem' in filters:
    #     if filters['ordem'] == 'nome':
    #         query = query.order_by(Products.name)
    #     elif filters['ordem'] == 'estoque':
    #         query = query.order_by(Products.stock)


    products = query.all() 
    print(products)
    return jsonify([product.as_dict() for product in products]) 

@bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Products(
        name=data['name'],
        price=data['price'],
        category=data['category'],
        stock=data['stock'],
        #image_url=data.get('image_url')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.as_dict()), 201

@bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = Products.query.get_or_404(product_id)
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    product.stock = data.get('stock', product.stock)
    # product.image_url = data.get('image_url', product.image_url)
    db.session.commit()
    return jsonify(product.as_dict())

@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
