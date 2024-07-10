from flask import Blueprint, request, jsonify
from ..models import Products
from sqlalchemy import asc,desc
from flask_jwt_extended import jwt_required
from .. import db

bp = Blueprint('products', __name__, url_prefix='/products')

@bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    filters = request.args
    query = Products.query

    if 'sem_estoque' in filters:
        query = query.filter(Products.stock == 0)
    
    if 'categoria' in filters:
        query = query.filter(Products.category == filters['categoria'])
    
    if 'nome' in filters:
        query = query.filter(Products.name.like(f"%{filters['nome']}%"))

    if 'product_id' in filters:
        query = query.filter(Products.id == filters['product_id'])

    if 'direcao' in filters:
        if 'ordem' in filters:
            if filters['ordem'] == 'nome':
                if 'direcao' in filters and filters['direcao'] == 'desc':
                    query = query.order_by(desc(Products.name))
                elif 'direcao' in filters and filters['direcao'] == 'asc':
                    query = query.order_by(asc(Products.name))
            elif filters['ordem'] == 'estoque':
                if filters['direcao'] == 'asc':
                    query = query.order_by(asc(Products.stock))
                elif filters['direcao'] == 'desc':
                    query = query.order_by(desc(Products.stock))
            elif filters['ordem'] == 'preco':
                if filters['direcao'] == 'asc':
                    query = query.order_by(asc(Products.price))
                elif filters['direcao'] == 'desc':
                    query = query.order_by(desc(Products.price))
    else:
        query = query.order_by(asc(Products.name))


    products = query.all() 
    return jsonify([product.as_dict() for product in products]) 

@bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    new_product = Products(
        name=data['name'],
        price=data['price'],
        category=data['category'],
        stock=data['stock'],
        image_url=data.get('image_url')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.as_dict()), 201

@bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.get_json()
    product = Products.query.get_or_404(product_id)
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    product.stock = data.get('stock', product.stock)
    product.active = data.get('active', product.active)
    product.image_url = data.get('image_url', product.image_url)
    db.session.commit()
    return jsonify(product.as_dict())

@bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
