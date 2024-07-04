from . import db
from datetime import datetime


class Products(db.Model):
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum('Bebida', 'Comida'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    #image_url = db.Column(db.String(200))
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Waiters(db.Model):
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)

class Tables(db.Model):
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True)
    in_use = db.Column(db.Boolean, default=False)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.id'))

class Order(db.Model):
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    id = db.Column(db.Integer, primary_key=True)
    waiter_id = db.Column(db.Integer, db.ForeignKey('waiter.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    products = db.Column(db.JSON, nullable=False)
    total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum('Pix', 'Cartao', 'Dinheiro'), nullable=False)
    status = db.Column(db.Enum('Aguardando', 'Pago', 'Entregue'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    finalized_at = db.Column(db.DateTime)
