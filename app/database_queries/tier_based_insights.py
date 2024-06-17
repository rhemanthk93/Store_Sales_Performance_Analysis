from sqlalchemy import text
from app import db
from app.utilities.currency_conversion import CurrencyConversion
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from kneed import KneeLocator
import json
import matplotlib.pyplot as plt


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


def determine_optimal_tiers(city_sales):
    # Plot to see the distribution
    # inspect_sales_distribution(city_sales)
    if isinstance(city_sales, dict):
        df = pd.DataFrame.from_dict(city_sales, orient='index', columns=['Total Sales'])
        sales_values = df['Total Sales'].astype(float).tolist()
    elif isinstance(city_sales, pd.DataFrame):
        sales_values = city_sales['Total Sales'].astype(float)
    else:
        raise ValueError("city_sales must be a dictionary or a pandas DataFrame.")

    sales_values_array = np.log1p(np.array(sales_values).reshape(-1, 1))

    inertias = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(sales_values_array)
        inertias.append(kmeans.inertia_)

    kl = KneeLocator(range(1, 11), inertias, curve="convex", direction="decreasing")
    optimal_k = kl.elbow if kl.elbow else 3

    return optimal_k


def create_sales_tiers():
    city_sales = fetch_and_convert_sales_data()
    optimal_k = determine_optimal_tiers(city_sales)

    if isinstance(city_sales, dict):
        df = pd.DataFrame.from_dict(city_sales, orient='index', columns=['Total Sales'])
        sales_values = df['Total Sales'].astype(float).tolist()
    elif isinstance(city_sales, pd.DataFrame):
        sales_values = city_sales['Total Sales'].astype(float)
    else:
        raise ValueError("Unexpected data type for city_sales.")

    sales_values_array = np.log1p(np.array(sales_values).reshape(-1, 1))

    kmeans = KMeans(n_clusters=optimal_k, random_state=0)
    kmeans.fit(sales_values_array)
    tier_labels = kmeans.labels_

    df_tiers = pd.DataFrame({'City': list(city_sales.keys()), 'Tier': tier_labels})
    df_tiers.set_index('City', inplace=True)
    json_data = df_tiers.to_dict(orient='index')

    return json.dumps(json_data)


def inspect_sales_distribution(city_sales):
    sales_values = list(city_sales.values())
    plt.hist(sales_values, bins=50)
    plt.xlabel('Total Sales (USD)')
    plt.ylabel('Number of Cities')
    plt.title('Sales Distribution Across Cities')
    plt.show()


def fetch_and_convert_order_timing_data():
    raw_sql = text('''
        SELECT ship_to_city_cd, EXTRACT(HOUR FROM order_time_pst) as order_hour, order_qty
        FROM `order`
    ''')
    results = db.session.execute(raw_sql).fetchall()

    order_timing_data = []
    for result in results:
        city = result[0]
        order_hour = result[1]
        order_qty = result[2]

        if order_hour is None or order_qty is None:
            continue

        order_timing_data.append({
            'city': city,
            'order_hour': order_hour,
            'order_qty': order_qty
        })

    return pd.DataFrame(order_timing_data)


def determine_optimal_clusters(order_data):
    order_agg = order_data.groupby(['city', 'order_hour']).agg({
        'order_qty': 'sum'
    }).reset_index()

    # Normalize the data
    order_agg_normalized = (order_agg[['order_hour', 'order_qty']] - order_agg[['order_hour', 'order_qty']].mean()) / \
                           order_agg[['order_hour', 'order_qty']].std()

    inertias = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(order_agg_normalized)
        inertias.append(kmeans.inertia_)

    kl = KneeLocator(range(1, 11), inertias, curve="convex", direction="decreasing")
    optimal_k = kl.elbow if kl.elbow else 3

    return optimal_k


def create_order_timing_clustering():
    order_data = fetch_and_convert_order_timing_data()
    optimal_k = determine_optimal_clusters(order_data)

    order_agg = order_data.groupby(['city', 'order_hour']).agg({
        'order_qty': 'sum'
    }).reset_index()

    order_agg_normalized = (order_agg[['order_hour', 'order_qty']] - order_agg[['order_hour', 'order_qty']].mean()) / \
                           order_agg[['order_hour', 'order_qty']].std()

    kmeans = KMeans(n_clusters=optimal_k, random_state=0)
    order_agg['cluster'] = kmeans.fit_predict(order_agg_normalized)

    return order_agg
