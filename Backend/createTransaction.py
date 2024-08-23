from flask import request, jsonify, session
from models import Transaction, db


def create_transaction():
    data = request.get_json()

    if 'username' not in session:
        #print("No username found in session")
        return jsonify({"message": "User not logged in!"}), 401

    #print("Session username:", session['username'])
    #print("Data received:", data)

    images = ",".join(data.get('images', []))
    product_name = data.get('product_name')
    phone_number = data.get('phone_number')
    price = data.get('price')
    url = data.get('url')
    order_details = data.get('order_details')
    username = session['username']  # Getting the username name from the session

    new_transaction = Transaction(
        images=images,
        product_name=product_name,
        phone_number=phone_number,
        price=price,
        url=url,
        order_details=order_details,
        username=username
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify(
        {"message": "Transaction created successfully", "transaction_id": new_transaction.transaction_id}), 201
