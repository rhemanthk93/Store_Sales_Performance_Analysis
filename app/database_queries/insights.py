from sqlalchemy import text
from app import db


def get_city_with_highest_per_hour_sales():
    raw_sql = text('''
        SELECT ship_to_city_cd, HOUR(order_time_pst) AS hour, SUM(rptg_amt) AS total_sales
        FROM `order`
        GROUP BY ship_to_city_cd, hour
        ORDER BY total_sales DESC;
    ''')
    results = db.session.execute(raw_sql).fetchall()

    sales_per_hour = [
        {
            'city': result[0],
            'hour': result[1],
            'total_sales': float(result[2])
        } for result in results
    ]

    return sales_per_hour


def get_city_with_highest_avg_sales():
    raw_sql = text('''
        SELECT ship_to_city_cd, AVG(rptg_amt) AS avg_sales
        FROM `order`
        GROUP BY ship_to_city_cd
        ORDER BY avg_sales DESC;
    ''')
    results = db.session.execute(raw_sql).fetchall()

    avg_sales = [
        {
            'city': result[0],
            'avg_sales': float(result[1])
        } for result in results
    ]

    return avg_sales