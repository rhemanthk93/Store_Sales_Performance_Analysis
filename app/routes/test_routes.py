from flask import Blueprint, jsonify
from app import db
from app.models.order import Order
from datetime import time

test = Blueprint('test', __name__)


@test.route('/')
def index():
    return "Hello, World!"


@test.route('/test_db')
def test_db():
    # Add a test order
    new_order = Order(
        order_id='12345',
        order_time_pst=time(12, 30, 0),
        city_district_id=None,
        ship_to_district_name='Test District',
        ship_to_city_cd='Test City',
        rptg_amt=100.0,
        currency_cd='USD',
        order_qty=1,
        data_source='Test'
    )
    db.session.add(new_order)
    db.session.commit()

    # Query the order
    order = Order.query.filter_by(order_id='12345').first()

    if order:
        return jsonify({
            'order_id': order.order_id,
            'order_time_pst': order.order_time_pst.strftime('%H:%M:%S') if order.order_time_pst else None,
            'city_district_id': order.city_district_id,
            'ship_to_district_name': order.ship_to_district_name,
            'ship_to_city_cd': order.ship_to_city_cd,
            'rptg_amt': order.rptg_amt,
            'currency_cd': order.currency_cd,
            'order_qty': order.order_qty,
            'data_source': order.data_source
        })
    else:
        return "Order not found", 404
