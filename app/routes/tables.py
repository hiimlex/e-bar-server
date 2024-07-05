from flask import Blueprint, request, jsonify
from sqlalchemy import desc,asc
from ..models import Tables
from flask_jwt_extended import jwt_required
from .. import db

bp = Blueprint('tables', __name__, url_prefix='/mesas')

@bp.route('', methods=['GET'])
@jwt_required()
def get_tables():
    filters = request.args
    query = Tables.query
    
    if 'direcao' in filters:
        if 'ordem' in filters:
            if filters['ordem'].lower() == 'numero':
                if filters['direcao'] == 'asc':
                    query = query.order_by(asc(Tables.id))
                elif filters['direcao'] == 'desc':
                    query = query.order_by(desc(Tables.id))
                

    tables = query.all()
    return jsonify([table.as_dict() for table in tables])

@bp.route('', methods=['POST'])
# @jwt_required()
def create_table():
    data = request.get_json()
    new_table = Tables(
        active=data.get('active', True),
        in_use=data.get('in_use', False),
        waiter_id=data.get('waiter_id'),
    )
    db.session.add(new_table)
    db.session.commit()
    return jsonify(new_table.as_dict()), 201

@bp.route('/<int:table_id>', methods=['PUT'])
@jwt_required()
def update_table(table_id):
    data = request.get_json()
    table = Tables.query.get_or_404(table_id)
    table.active = data.get('active', table.active)
    table.in_use = data.get('in_use', table.in_use)
    table.waiter_id = data.get('waiter_id', table.waiter_id)
    db.session.commit()
    return jsonify(table.as_dict())

@bp.route('/<int:table_id>', methods=['DELETE'])
@jwt_required()
def delete_table(table_id):
    table = Tables.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return '', 204
