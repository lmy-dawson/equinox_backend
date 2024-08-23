from flask import request, jsonify
from models import User, db
from werkzeug.security import generate_password_hash

def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    mobile_number = data.get('mobile_number')
    password = data.get('password')

    if User.query.filter_by(email=email).first() or User.query.filter_by(mobile_number=mobile_number).first():
        return jsonify({'message': 'User already exists!'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, mobile_number=mobile_number, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201
