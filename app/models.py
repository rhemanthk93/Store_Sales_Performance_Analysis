from app import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(64), unique=True, nullable=False)
    order_time = db.Column(db.Time, nullable=False)
    district = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
