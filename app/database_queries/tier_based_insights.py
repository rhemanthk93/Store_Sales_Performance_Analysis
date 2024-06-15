from sqlalchemy import text
from app import db
from app.utilities.currency_conversion import CurrencyConversion
from decimal import Decimal
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer
import json


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