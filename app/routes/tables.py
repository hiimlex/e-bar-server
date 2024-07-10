from flask import Blueprint, request, jsonify
from sqlalchemy import desc,asc, false, true
from ..models import Tables, Waiters
from flask_jwt_extended import jwt_required
from sqlalchemy.sql.expression import false
from .. import db

bp = Blueprint('tables', __name__, url_prefix='/tables')

@bp.route('', methods=['GET'])
@jwt_required()
def get_tables():
    filters = request.args
    query = db.session.query(
        Tables,
        Waiters.name.label('waiter_name')   
    ).outerjoin(Waiters, Waiters.id == Tables.waiter_id
    )

    if 'in_use' in filters:
        in_use_value = filters['in_use'].lower() == 'true'
        query = query.filter(Tables.in_use == in_use_value)
    
    if 'is_active' in filters:
        active_value = filters['is_active'].lower() == 'true'
        query = query.filter(Tables.is_active == active_value)
    
    if 'sort_key' in filters:
        if 'sort' in filters:
            if filters['sort_key'].lower() == 'id':
                if filters['sort'] == 'asc':
                    query = query.order_by(asc(Tables.id))
                elif filters['sort'] == 'desc':
                    query = query.order_by(desc(Tables.id))
                

    tables = query.all()

    tables_list = []
    for table, waiter_name in tables:
        table_dict = table.as_dict()
        table_dict['waiter_name'] = waiter_name
        tables_list.append(table_dict)

    return jsonify(tables_list)

@bp.route('', methods=['POST'])
@jwt_required()
def create_table():
    data = request.get_json()
    new_table = Tables(
        is_active=data.get('is_active', True),
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
