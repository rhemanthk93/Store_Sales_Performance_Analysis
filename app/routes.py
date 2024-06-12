from flask import Blueprint, jsonify
from app import db
from app.models import Order
from datetime import time

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return "Hello, World!"


@main.route('/test_db')
def test_db():
    # Add a test order
    new_order = Order(order_id='12345', order_time=time(12, 30, 0), district='Test District', city='Test City',
                      amount=100.0, currency='USD', quantity=1)
    db.session.add(new_order)
    db.session.commit()

    # Query the order
    order = Order.query.filter_by(order_id='12345').first()

    if order:
        return jsonify({
            'order_id': order.order_id,
            'order_time': order.order_time.strftime('%H:%M:%S'),
            'district': order.district,
            'city': order.city,
            'amount': order.amount,
            'currency': order.currency,
            'quantity': order.quantity
        })
    else:
        return "Order not found", 404
