from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import deferred, relationship
from sqlalchemy import func, Enum

class Products(db.Model):
    __tablename__ = 'products'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum('Cervejas', 'Comidas', 'Destilados', 'Refrigerantes', 'Petiscos'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(400))
    order_products = relationship('OrderProducts', backref='products', lazy=True)

class Waiters(db.Model):
    __tablename__ = 'waiters'

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
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    orders = relationship('Orders', backref='waiters', lazy=True)
    tables = relationship('Tables', backref='waiters', lazy=True)

class Tables(db.Model):
    __tablename__ = 'tables'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=True)
    in_use = db.Column(db.Boolean, default=False)

    waiter_id = db.Column(db.Integer, db.ForeignKey('waiters.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))

class Orders(db.Model):
    __tablename__ = 'orders'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiters.id'), nullable=False)
    table_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10, 2), default=0)
    payment_method = db.Column(Enum('pix', 'card', 'cash'))
    status = db.Column(Enum('on_demand', 'pending', 'finished'), nullable=False, default='on_demand')
    finalized_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), server_onupdate=func.now())
    customers = db.Column(db.Integer, default=0)

    order_products = relationship('OrderProducts', backref='orders', lazy=True, cascade='all, delete-orphan')

class OrderProducts(db.Model):
    __tablename__ = 'order_products'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(Enum('ordered', 'delivered'), nullable=False, default='ordered')
    delivered = db.Column(db.Integer, default=0)