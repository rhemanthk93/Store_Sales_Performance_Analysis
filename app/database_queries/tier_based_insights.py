from sqlalchemy import text
from app import db
from app.utilities.currency_conversion import CurrencyConversion
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer


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

        if amount_usd is None:
            continue

        if city not in city_sales:
            city_sales[city] = 0
        city_sales[city] += amount_usd

    return city_sales


def create_sales_tiers():
    city_sales = fetch_and_convert_sales_data()

    # Convert to DataFrame
    df = pd.DataFrame(list(city_sales.items()), columns=['City', 'Total Sales'])

    # Apply Binning
    est = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile')
    df['Tier'] = est.fit_transform(df[['Total Sales']])

    # Map bins to tier names
    tier_mapping = {0: 'Low Spending', 1: 'Medium Spending', 2: 'High Spending'}
    df['Tier'] = df['Tier'].map(tier_mapping)

    # Convert DataFrame to JSON
    tiers_json = df.to_json(orient='records')

    return tiers_json


def fetch_order_frequency_data():
    raw_sql = text('''
        SELECT ship_to_city_cd, COUNT(order_id) as order_count
        FROM `order`
        GROUP BY ship_to_city_cd
    ''')
    results = db.session.execute(raw_sql).fetchall()

    city_orders = {result[0]: result[1] for result in results}
    return city_orders


def create_order_frequency_tiers():
    city_orders = fetch_order_frequency_data()

    # Convert the city orders dictionary to a DataFrame
    df = pd.DataFrame(list(city_orders.items()), columns=['City', 'Order Count'])

    # Apply Binning using KBinsDiscretizer
    est = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile')
    df['Tier'] = est.fit_transform(df[['Order Count']])

    # Map the numeric bins to descriptive tier names
    tier_mapping = {0: 'Low Order Frequency', 1: 'Medium Order Frequency', 2: 'High Order Frequency'}
    df['Tier'] = df['Tier'].map(tier_mapping)

    # Convert the DataFrame to JSON
    tiers_json = df.to_json(orient='records')

    return tiers_json


def fetch_transaction_currency_data():
    raw_sql = text('''
        SELECT ship_to_city_cd, currency_cd, COUNT(order_id) as transaction_count
        FROM `order`
        GROUP BY ship_to_city_cd, currency_cd
    ''')
    results = db.session.execute(raw_sql).fetchall()

    city_currency_data = {}
    for result in results:
        city = result[0]
        currency = result[1]
        count = result[2]

        if city not in city_currency_data:
            city_currency_data[city] = {'USD': 0, 'RMB': 0}

        city_currency_data[city][currency] = count

    return city_currency_data


def create_currency_based_tiers():
    city_currency_data = fetch_transaction_currency_data()

    # Convert the city currency data dictionary to a DataFrame
    df = pd.DataFrame.from_dict(city_currency_data, orient='index').reset_index()
    df.columns = ['City', 'USD Transactions', 'RMB Transactions']

    # Determine dominant currency for each city
    def determine_tier(row):
        if row['USD Transactions'] > row['RMB Transactions']:
            return 'USD Dominant'
        elif row['RMB Transactions'] > row['USD Transactions']:
            return 'RMB Dominant'
        else:
            return 'Mixed Currency'

    df['Tier'] = df.apply(determine_tier, axis=1)

    # Convert the DataFrame to JSON
    tiers_json = df.to_json(orient='records')

    return tiers_json


def fetch_peak_hour_data():
    conversion = CurrencyConversion()

    raw_sql = text('''
        SELECT ship_to_city_cd, EXTRACT(HOUR FROM order_time_pst) as hour, rptg_amt, currency_cd
        FROM `order`
    ''')
    results = db.session.execute(raw_sql).fetchall()

    peak_hour_data = []
    for result in results:
        city = result[0]
        hour = result[1]
        amount_usd = conversion.convert_to_usd(result[2], result[3])
        if amount_usd is not None:
            peak_hour_data.append({'city': city, 'hour': hour, 'total_sales_usd': float(amount_usd)})

    return peak_hour_data


def create_peak_hour_tiers():
    peak_hour_data = fetch_peak_hour_data()

    df = pd.DataFrame(peak_hour_data)

    # Identify peak hours (e.g., 8-10 AM)
    df['Peak'] = df['hour'].apply(lambda x: 'Peak' if 8 <= x <= 10 else 'Off-Peak')

    peak_sales = df[df['Peak'] == 'Peak'].groupby('city')['total_sales_usd'].sum().reset_index()
    off_peak_sales = df[df['Peak'] == 'Off-Peak'].groupby('city')['total_sales_usd'].sum().reset_index()

    peak_sales['Peak_Sales'] = peak_sales['total_sales_usd']
    off_peak_sales['Off_Peak_Sales'] = off_peak_sales['total_sales_usd']

    combined_sales = pd.merge(peak_sales[['city', 'Peak_Sales']], off_peak_sales[['city', 'Off_Peak_Sales']], on='city',
                              how='outer').fillna(0)

    combined_sales['Total_Sales'] = combined_sales['Peak_Sales'] + combined_sales['Off_Peak_Sales']
    combined_sales['Tier'] = combined_sales.apply(
        lambda x: 'Peak Hour Cities' if x['Peak_Sales'] > x['Off_Peak_Sales'] else 'Off-Peak Hour Cities', axis=1)

    tiers_json = combined_sales.to_json(orient='records')

    return tiers_json