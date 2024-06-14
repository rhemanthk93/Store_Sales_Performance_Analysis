from app import db

class Order(db.Model):
    order_id = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    order_time_pst = db.Column(db.Time, nullable=True)
    city_district_id = db.Column(db.String(255), nullable=True)
    ship_to_district_name = db.Column(db.String(255), nullable=True)
    ship_to_city_cd = db.Column(db.String(255), nullable=True)
    rptg_amt = db.Column(db.Numeric(10, 2), nullable=True)
    currency_cd = db.Column(db.String(10), nullable=True)
    order_qty = db.Column(db.Integer, nullable=True)
    data_source = db.Column(db.String(10), nullable=False)



# Explanation:
# order_id: Set as the primary key, unique, and not nullable.
# order_time_pst: Can be nullable to handle cases where the time is not available or invalid.
# city_district_id: Nullable to handle rows from the JSON file where this value is not available.
# ship_to_district_name: Nullable to handle rows from the Excel file where this value is not available.
# ship_to_city_cd: Nullable to handle rows from the Excel file where this value is not available.
# rptg_amt: Nullable to handle cases where the reporting amount might be missing.
# currency_cd: Nullable to handle cases where the currency code might be missing.
# order_qty: Nullable to handle cases where the order quantity might be missing.
# data_source: Indicates the source of the data ('Excel' or 'JSON'); it is not nullable because every row should have a source.