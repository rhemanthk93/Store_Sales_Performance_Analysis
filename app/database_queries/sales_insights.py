from sqlalchemy import text
from app import db
from app.utilities.currency_conversion import CurrencyConversion


def fetch_and_convert_sales_data_by_city():
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
    city_sales = fetch_and_convert_sales_data_by_city()

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


def fetch_and_convert_sales_data_by_city_and_district():
    conversion = CurrencyConversion()

    raw_sql = text('''
        SELECT ship_to_city_cd, ship_to_district_name, rptg_amt, currency_cd
        FROM `order`
    ''')
    results = db.session.execute(raw_sql).fetchall()

    city_sales = {}
    for result in results:
        city = result[0]
        district = result[1]
        amount_usd = conversion.convert_to_usd(result[2], result[3])
        amount_rmb = conversion.convert_to_rmb(result[2], result[3])

        if amount_usd is None or amount_rmb is None:
            continue

        if city not in city_sales:
            city_sales[city] = {'usd': [], 'rmb': [], 'districts': set(), 'hours': 0}

        city_sales[city]['usd'].append(amount_usd)
        city_sales[city]['rmb'].append(amount_rmb)
        city_sales[city]['districts'].add(district)
        city_sales[city]['hours'] += 1

    return city_sales


def get_city_with_highest_avg_sales_by_district():
    city_sales = fetch_and_convert_sales_data_by_city_and_district()

    highest_avg_sales = []
    for city, sales in city_sales.items():
        avg_sales_usd = sum(sales['usd']) / len(sales['usd'])
        avg_sales_rmb = sum(sales['rmb']) / len(sales['rmb'])
        highest_avg_sales.append({
            'city': city,
            'districts': list(sales['districts']),
            'avg_sales_usd': float(avg_sales_usd),
            'avg_sales_rmb': float(avg_sales_rmb)
        })

    highest_avg_sales.sort(key=lambda x: x['avg_sales_usd'], reverse=True)
    return highest_avg_sales


def fetch_and_convert_time_based_sales_data():
    conversion = CurrencyConversion()

    raw_sql = text('''
        SELECT ship_to_city_cd, rptg_amt, currency_cd, HOUR(order_time_pst) AS hour
        FROM `order`
    ''')
    results = db.session.execute(raw_sql).fetchall()

    time_based_sales = {}
    for result in results:
        city = result[0]
        hour = result[3]
        amount_usd = conversion.convert_to_usd(result[1], result[2])
        amount_rmb = conversion.convert_to_rmb(result[1], result[2])

        if amount_usd is None or amount_rmb is None:
            continue

        if city not in time_based_sales:
            time_based_sales[city] = {'usd': {}, 'rmb': {}}

        if hour not in time_based_sales[city]['usd']:
            time_based_sales[city]['usd'][hour] = 0
            time_based_sales[city]['rmb'][hour] = 0

        time_based_sales[city]['usd'][hour] += amount_usd
        time_based_sales[city]['rmb'][hour] += amount_rmb

    return time_based_sales


def get_time_based_sales_trend():
    time_based_sales = fetch_and_convert_time_based_sales_data()

    time_based_sales_trend = []
    for city, sales in time_based_sales.items():
        for hour in sales['usd'].keys():
            time_based_sales_trend.append({
                'city': city,
                'hour': hour,
                'total_sales_usd': float(sales['usd'][hour]),
                'total_sales_rmb': float(sales['rmb'][hour])
            })

    return time_based_sales_trend


def fetch_and_convert_sales_by_region():
    conversion = CurrencyConversion()

    raw_sql = text('''
        SELECT ship_to_district_name, rptg_amt, currency_cd
        FROM `order`
    ''')
    results = db.session.execute(raw_sql).fetchall()

    region_sales = {}
    for result in results:
        region = result[0]
        amount_usd = conversion.convert_to_usd(result[1], result[2])
        amount_rmb = conversion.convert_to_rmb(result[1], result[2])

        if amount_usd is None or amount_rmb is None:
            continue

        if region not in region_sales:
            region_sales[region] = {'usd': 0, 'rmb': 0}

        region_sales[region]['usd'] += amount_usd
        region_sales[region]['rmb'] += amount_rmb

    return region_sales


def get_top_sales_by_region():
    region_sales = fetch_and_convert_sales_by_region()

    top_sales_by_region = []
    for region, sales in region_sales.items():
        top_sales_by_region.append({
            'region': region,
            'total_sales_usd': float(sales['usd']),
            'total_sales_rmb': float(sales['rmb'])
        })

    top_sales_by_region.sort(key=lambda x: x['total_sales_usd'], reverse=True)
    return top_sales_by_region
