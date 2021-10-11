from flask import Flask, request, jsonify
from service import insert_library, insert_book, insert_user, create_checkin_book, create_checkout_book, list_of_checkout_book_by_id
app = Flask(__name__)

@app.route('/api/library/create', methods=['post'])
def add_library():
    library = request.get_json()
    return jsonify(insert_library(library))

@app.route('/api/book/create', methods=['post'])
def add_book():
    book = request.get_json()
    return jsonify(insert_book(book))

@app.route('/api/user/create', methods=['post'])
def add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/book/checkin', methods=['post'])
def book_checkin():
    checkin = request.get_json()
    return jsonify(create_checkin_book(checkin))

@app.route('/api/book/checkout', methods=['post'])
def book_checkout():
    checkout = request.get_json()
    return jsonify(create_checkout_book(checkout))

@app.route('/api/book/checkout', methods=['get'])
def list_of_book_checkout():
    user_detail = request.args.get("name")
    return jsonify(list_of_checkout_book_by_id(user_detail))


