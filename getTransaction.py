from datetime import datetime

from flask import request, jsonify, session, url_for
from models import Transaction, db, Payment


# Get all transactions
def get_all_transactions():
    if 'username' not in session:
        return jsonify({"message": "User not logged in!"}), 401

    username = session['username']
    transactions = Transaction.query.filter_by(username=username).all()

    transactions_data = []
    for transaction in transactions:
        transaction_dict = {
            "transaction_id": transaction.transaction_id,
            "product_name": transaction.product_name,
            "amount": transaction.price,
            "status": transaction.status,
            "time": transaction.date_created,
            "seller": transaction.username
        }
        print(transaction_dict)
        transactions_data.append(transaction_dict)

    print("All transactions data:", transactions_data)

    return jsonify({"transactions": transactions_data}), 200


# Get transaction details from the transaction id
def get_transaction(transaction_id):
    if 'username' not in session:
        return jsonify({"message": "User not logged in!"}), 401

    username = session['username']
    transaction = Transaction.query.filter_by(transaction_id=transaction_id, status=1).first()

    if not transaction:
        return jsonify({"message": "Transaction not found!"}), 404

    # Split the comma-separated images string back into a list
    image_filenames = transaction.images.split(',')

    # Generate the full URLs for each image
    image_urls = [url_for('static', filename=f'uploads/{filename}', _external=True) for filename in image_filenames]

    transaction_data = {
        "transaction_id": transaction.transaction_id,
        "product_name": transaction.product_name,
        "images": image_urls,
        "amount": transaction.price,
        "status": transaction.status,
        "time": transaction.date_created,
        "seller": transaction.username,
        "phone_number": transaction.phone_number,  # Include additional fields as needed
        "url": transaction.url,
        "order_details": transaction.order_details,
    }
    return jsonify(transaction_data), 200


# GET ONGOING TRANSACTIONS
def get_ongoing_transactions():
    if 'username' not in session:
        return jsonify({"message": "User not logged in!"}), 401

    username = session['username']

    # Get transactions where status is 2
    transactions = Transaction.query.filter_by(status=2).all()

    transactions_data = []
    for transaction in transactions:
        # Check if the user is the creator or has created a payment for the transaction
        if transaction.username == username or Payment.query.filter_by(transaction_id=transaction.transaction_id,
                                                                       buyer_name=username).first():
            transaction_dict = {
                "transaction_id": str(transaction.transaction_id),
                "product_name": transaction.product_name,
                "amount": float(transaction.price),
                "status": int(transaction.status),
                "time": transaction.date_created,
                "seller": transaction.username,
            }
            transactions_data.append(transaction_dict)
    print("Filtered transactions data:", transactions_data)

    return jsonify({"transactions": transactions_data}), 200


# GETTING ALL THE TRANSACTION DETAILS FROM THE PAYMENT AND TRANSACTION
def get_transaction_details(transaction_id):
    if 'username' not in session:
        return jsonify({"message": "User not logged in!"}), 401

    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    payment = Payment.query.filter_by(transaction_id=transaction_id).first()

    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    if transaction.username != session['username'] and (not payment or payment.buyer_name != session['username']):
        return jsonify({"message": "You are not authorized to view this transaction"}), 403

    transaction_data = {
        "transaction_id": str(transaction.transaction_id),
        "product_name": transaction.product_name,
        "amount": float(transaction.price),
        "status": int(transaction.status),
        "time": transaction.date_created.isoformat(),
        "seller": transaction.username,
        "seller_number": transaction.phone_number,
        "url": transaction.url,
        "order_details": transaction.order_details

    }

    payment_data = None
    if payment:
        payment_data = {
            "payment_method": payment.payment_method,
            "amount": float(payment.amount),
            "buyer_name": payment.buyer_name,
            "buyer_number": payment.phone_number,
            "address": payment.address
        }

    return jsonify({"transaction": transaction_data, "payment": payment_data}), 200


def complete_transaction():
    data = request.get_json()
    transaction_id = data.get('transaction_id')

    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()

    if transaction:
        transaction.status = 3  # Set status to delivered
        transaction.date_completed = datetime.utcnow()  # Set the completion date
        db.session.commit()

        return jsonify({'message': 'Transaction marked as received'}), 200
    else:
        return jsonify({'message': 'Transaction not found'}), 404
