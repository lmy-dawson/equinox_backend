from flask import request, jsonify, session
from models import Transaction, Payment, db
from sqlalchemy.exc import IntegrityError


def create_payment():
    data = request.get_json()

    if 'username' not in session:
        return jsonify({"message": "User not logged in!"}), 401

    amount = data.get('amount')
    payment_method = data.get('paymentMethod')
    phone_number = data.get('phoneNumber')
    buyer_number = data.get('phoneNumber')
    buyer_name = session['username']
    address = data.get('address')
    transaction_id = data.get('transactionId')

    print(f"Received data: {data}")
    # Make sure to handle the missing fields and defaults
    # if not all([amount, payment_method, phone_number, address, transaction_id]):
    # return jsonify({"message": "Missing required fields"}), 400

    # Find the transaction to update
    try:
        db.session.begin()

        transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
        if not transaction:
            db.session.rollback()  # Rollback if transaction is not found
            return jsonify({'message': 'Transaction not found'}), 404

        new_payment = Payment(
            amount=amount,
            payment_method=payment_method,
            phone_number=phone_number,
            buyer_number=buyer_number,
            buyer_name=buyer_name,
            address=address,
            transaction_id=transaction.transaction_id
        )

        print(f"Creating new payment: {new_payment}")
        # Add payment to the database
        db.session.add(new_payment)

            # Update transaction status
        transaction.status = 2  # Update status to 2 for 'ongoing'
        db.session.commit()

        return jsonify({"message": "Payment successfully made", "payment_id": new_payment.payment_id}), 201

    except IntegrityError as e:
        db.session.rollback()  # Rollback in case of integrity error
        print(f"IntegrityError: {e}")
        return jsonify({"message": "Integrity error occurred"}), 400
    except Exception as e:
        db.session.rollback()  # Rollback in case of other errors
        print(f"Exception: {e}")
        return jsonify({"message": str(e)}), 500
