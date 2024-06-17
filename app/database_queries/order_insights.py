from sqlalchemy import text
from app import db


def fetch_time_based_order_data_by_city():
    raw_sql = text('''
        SELECT ship_to_city_cd, HOUR(order_time_pst) AS hour, COUNT(*) as order_count
        FROM `order`
        GROUP BY ship_to_city_cd, hour
        ORDER BY ship_to_city_cd, hour;
    ''')
    results = db.session.execute(raw_sql).fetchall()

    time_based_orders = {}
    for result in results:
        city = result[0]
        hour = result[1]
        order_count = result[2]

        if city not in time_based_orders:
            time_based_orders[city] = {}

        time_based_orders[city][hour] = order_count

    return time_based_orders


def get_time_based_order_trend_by_city():
    time_based_orders = fetch_time_based_order_data_by_city()

    time_based_order_trend = []
    for city, orders in time_based_orders.items():
        for hour, order_count in orders.items():
            time_based_order_trend.append({
                'city': city,
                'hour': hour,
                'order_count': order_count
            })

    return time_based_order_trend


def fetch_order_data_by_region():
    raw_sql = text('''
        SELECT ship_to_district_name, COUNT(*) as order_count
        FROM `order`
        GROUP BY ship_to_district_name
    ''')
    results = db.session.execute(raw_sql).fetchall()

    region_orders = {}
    for result in results:
        region = result[0]
        order_count = result[1]

        region_orders[region] = order_count

    return region_orders


def get_orders_by_region():
    region_orders = fetch_order_data_by_region()

    orders_by_region = []
    for region, order_count in region_orders.items():
        orders_by_region.append({
            'region': region,
            'order_count': order_count
        })

    orders_by_region.sort(key=lambda x: x['order_count'], reverse=True)
    return orders_by_region
