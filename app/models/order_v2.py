from app import db

class Order_v2(db.Model):
    order_id = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    order_time_pst = db.Column(db.Time, nullable=True)
    order_date = db.Column(db.Date, nullable=True)
    customer_id = db.Column(db.String(255), nullable=True)
    customer_type = db.Column(db.String(50), nullable=True)
    product_id = db.Column(db.String(255), nullable=True)
    product_category = db.Column(db.String(255), nullable=True)
    city_district_id = db.Column(db.String(255), nullable=True)
    ship_to_district_name = db.Column(db.String(255), nullable=True)
    ship_to_city_cd = db.Column(db.String(255), nullable=True)
    region = db.Column(db.String(255), nullable=True)
    rptg_amt = db.Column(db.Numeric(10, 2), nullable=True)
    discount_amt = db.Column(db.Numeric(10, 2), nullable=True)
    currency_cd = db.Column(db.String(10), nullable=True)
    order_qty = db.Column(db.Integer, nullable=True)
    data_source = db.Column(db.String(10), nullable=False)
    order_status = db.Column(db.String(50), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)
    payment_status = db.Column(db.String(50), nullable=True)
    delivery_date = db.Column(db.Date, nullable=True)
    delivery_method = db.Column(db.String(50), nullable=True)

# Explanation:
# order_id: Set as the primary key, unique, and not nullable.
# order_time_pst: Can be nullable to handle cases where the time is not available or invalid.
# order_date: To analyze orders over time.
# customer_id: To track customer orders and analyze customer behavior.
# customer_type: To categorize customers.
# product_id: To track which products are ordered.
# product_category: To analyze orders by product categories.
# city_district_id: Nullable to handle rows from the JSON file where this value is not available.
# ship_to_district_name: Nullable to handle rows from the Excel file where this value is not available.
# ship_to_city_cd: Nullable to handle rows from the Excel file where this value is not available.
# region: To analyze orders by broader geographical regions.
# rptg_amt: Nullable to handle cases where the reporting amount might be missing.
# discount_amt: To analyze the impact of discounts on sales.
# currency_cd: Nullable to handle cases where the currency code might be missing.
# order_qty: Nullable to handle cases where the order quantity might be missing.
# data_source: Indicates the source of the data ('Excel' or 'JSON'); it is not nullable because every row should have a source.
# order_status: To track the status of the order.
# payment_method: To analyze the preferred payment methods.
# payment_status: To track the payment status.
# delivery_date: To track when orders are delivered.
# delivery_method: To analyze the preferred delivery methods.