from . import db
from datetime import datetime
from sqlalchemy.orm import deferred

class Products(db.Model):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum('Cervejas', 'Comidas', 'Destilados', 'Refrigerantes', 'Petiscos'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(400))

class Waiters(db.Model):
    def as_dict(self):            
         # Lista de nomes das colunas que você deseja incluir no dicionário
        columns_to_include = ['id', 'name', 'email', 'phone', 'active', 'is_admin']
        
        # Criando o dicionário com apenas as colunas desejadas
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name in columns_to_include}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = deferred(db.Column(db.String(100), nullable=False))
    active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

class Tables(db.Model):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    in_use = db.Column(db.Boolean, default=False)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiters.id'))

class Order(db.Model):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    products = db.Column(db.JSON, nullable=False)
    total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum('Pix', 'Cartao', 'Dinheiro'), nullable=False)
    status = db.Column(db.Enum('Aguardando', 'Pago'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    finalized_at = db.Column(db.DateTime)
