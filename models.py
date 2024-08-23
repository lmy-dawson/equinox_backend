from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import uuid
from datetime import datetime

db = SQLAlchemy()
engine = create_engine('sqlite:///database.db', connect_args={'timeout': 15})

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, mobile_number, password):
        self.username = username
        self.email = email
        self.mobile_number = mobile_number
        self.password = password


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    images = db.Column(db.Text, nullable=False)  # Store image URIs as a comma-separated string
    product_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String(200), nullable=True)
    order_details = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default=1)  # 1 for 'created'
    username = db.Column(db.String(50), nullable=False)
    date_completed = db.Column(db.DateTime, nullable=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(10), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, default=1)  # 1 for 'paid'
    buyer_name = db.Column(db.String(100), nullable=False)
    buyer_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    transaction = db.relationship('Transaction', backref='payments')


