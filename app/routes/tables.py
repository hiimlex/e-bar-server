from flask import Blueprint, request, jsonify
from ..models import Tables
from .. import db

bp = Blueprint('tables', __name__, url_prefix='/table')

@bp.route('', methods=['GET'])
def get_tables():
    filters = request.args
    query = Tables.query
    
    if 'ordem' in filters:
        if filters['ordem'] == 'numero':
            query = query.order_by(Tables.number)

    tables = query.all()
    return jsonify([table.as_dict() for table in tables])

@bp.route('', methods=['POST'])
def create_table():
    data = request.get_json()
    new_table = Tables(
        number=data['number'],
        active=data.get('active', True),
        in_use=data.get('in_use', False),
        waiter_id=data.get('waiter_id')
    )
    db.session.add(new_table)
    db.session.commit()
    return jsonify(new_table.as_dict()), 201

@bp.route('/<int:table_id>', methods=['PUT'])
def update_table(table_id):
    data = request.get_json()
    table = Tables.query.get_or_404(table_id)
    table.number = data.get('number', table.number)
    table.active = data.get('active', table.active)
    table.in_use = data.get('in_use', table.in_use)
    table.waiter_id = data.get('waiter_id', table.waiter_id)
    db.session.commit()
    return jsonify(table.as_dict())

@bp.route('/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    table = Tables.query.get_or_404(table_id)
    db.session.delete(table)
    db.session.commit()
    return '', 204
