from flask import Flask, jsonify
from models import db
from signup import register_user, db
from login import login_user, get_current_user, logout_user, db
from createTransaction import create_transaction, db
from createPayment import create_payment, db
from getTransaction import get_all_transactions, get_transaction, get_ongoing_transactions, get_transaction_details, complete_transaction
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration for SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set a secret key for session management
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a random secret key

db.init_app(app)


# Root route
@app.route('/')
def index():
    return jsonify({"message": "EQUINOX BACKEND  API!"})


# Register Blueprints or routes
app.add_url_rule('/register', 'register_user', register_user, methods=['POST'])
app.add_url_rule('/login', 'login_user', login_user, methods=['POST'])
app.add_url_rule('/current_user', 'get_current_user', get_current_user, methods=['GET'])
app.add_url_rule('/logout', 'logout_user', logout_user, methods=['POST'])
app.add_url_rule('/create_transaction', 'create_transaction', create_transaction, methods=['POST'])
app.add_url_rule('/create_payment', 'create_payment', create_payment, methods=['POST'])
app.add_url_rule('/get_all_transactions', 'get_all_transactions', get_all_transactions, methods=['GET'])
app.add_url_rule('/get_transaction/<transaction_id>', 'get_transactions', get_transaction, methods=['GET'])
app.add_url_rule('/get_ongoing_transactions', 'get_ongoing_transactions', get_ongoing_transactions, methods=['GET'])
app.add_url_rule('/get_details/<transaction_id>', 'get_transaction_details', get_transaction_details, methods=['GET'])
app.add_url_rule('/complete_transaction', 'complete_transaction', complete_transaction, methods=['POST'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run()
