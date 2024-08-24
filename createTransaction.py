from flask import request, jsonify, session, url_for
from models import Transaction, db
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_transaction():
    if 'username' not in session:
        # print("No username found in session")
        return jsonify({"message": "User not logged in!"}), 401

    data = request.form  # Use form data for image and JSON data

    # Handle image upload
    file = request.files.get('images')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)


        # Create the correct URL for the image
        file_url = url_for('static', filename=f'uploads/{filename}', _external=True)
    else:
        return jsonify({"message": "Image upload failed!"}), 400

    # images = ",".join(data.get('images', []))
    product_name = data.get('product_name')
    phone_number = data.get('phone_number')
    price = data.get('price')
    url = data.get('url')
    order_details = data.get('order_details')
    username = session['username']  # Getting the username name from the session

    new_transaction = Transaction(
        images=file_url,  # Save the file path instead of image data
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
