from flask import request, jsonify, session
from werkzeug.security import check_password_hash
from models import User, db


def login_user():
    data = request.get_json()
    mobile_number = data.get('mobile_number')
    password = data.get('password')

    user = User.query.filter_by(mobile_number=mobile_number).first()

    if user and check_password_hash(user.password, password):
        session['username'] = user.username  # Store username in session
        print("Session username:", session['username'])
        return jsonify({"message": "Login successful!"}), 200

    elif user:
        return jsonify({"message": "Invalid password!"}), 401
    else:
        return jsonify({"message": "User doesn't exist!"}), 404


def get_current_user():
    if 'username' in session:
        return jsonify({"username": session['username']}), 200
    else:
        return jsonify({"message": "User not logged in!"}), 401


def logout_user():
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully"}), 200
