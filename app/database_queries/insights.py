# app/database_queries/insights.py
from sqlalchemy import text
from app import db
from app.utilities.currency_conversion import CurrencyConversion
from decimal import Decimal


def fetch_and_convert_sales_data():
    conversion = CurrencyConversion()

    raw_sql = text('''
        SELECT ship_to_city_cd, rptg_amt, currency_cd
        FROM `order`
    ''')
    results = db.session.execute(raw_sql).fetchall()

    city_sales = {}
    for result in results:
        city = result[0]
        amount_usd = conversion.convert_to_usd(result[1], result[2])
        amount_rmb = conversion.convert_to_rmb(result[1], result[2])

        if amount_usd is None or amount_rmb is None:
            continue

        if city not in city_sales:
            city_sales[city] = {'usd': [], 'rmb': [], 'hours': 0}

        city_sales[city]['usd'].append(amount_usd)
        city_sales[city]['rmb'].append(amount_rmb)
        city_sales[city]['hours'] += 1

    return city_sales


def get_city_with_highest_per_hour_sales():
    city_sales = fetch_and_convert_sales_data()

    highest_per_hour_sales = []
    for city, sales in city_sales.items():
        total_sales_usd = sum(sales['usd'])
        total_sales_rmb = sum(sales['rmb'])
        avg_hourly_sales_usd = total_sales_usd / sales['hours']
        avg_hourly_sales_rmb = total_sales_rmb / sales['hours']
        highest_per_hour_sales.append({
            'city': city,
            'avg_hourly_sales_usd': float(avg_hourly_sales_usd),
            'avg_hourly_sales_rmb': float(avg_hourly_sales_rmb)
        })

    highest_per_hour_sales.sort(key=lambda x: x['avg_hourly_sales_usd'], reverse=True)
    return highest_per_hour_sales


def get_city_with_highest_avg_sales():
    city_sales = fetch_and_convert_sales_data()

    highest_avg_sales = []
    for city, sales in city_sales.items():
        avg_sales_usd = sum(sales['usd']) / len(sales['usd'])
        avg_sales_rmb = sum(sales['rmb']) / len(sales['rmb'])
        highest_avg_sales.append({
            'city': city,
            'avg_sales_usd': float(avg_sales_usd),
            'avg_sales_rmb': float(avg_sales_rmb)
        })

    highest_avg_sales.sort(key=lambda x: x['avg_sales_usd'], reverse=True)
    return highest_avg_sales