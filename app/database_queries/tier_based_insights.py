from sqlalchemy import text
from app import db
from app.utilities.currency_conversion import CurrencyConversion
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
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


def determine_optimal_tiers(city_sales):
    # Check if city_sales is a dictionary or DataFrame
    if isinstance(city_sales, dict):
        # Convert city_sales to a DataFrame (assuming it's a dictionary)
        df = pd.DataFrame.from_dict(city_sales, orient='index', columns=['Total Sales'])
        sales_values = df['Total Sales'].tolist()  # Extract sales column as a list

    elif isinstance(city_sales, pd.DataFrame):
        # Assuming city_sales is a DataFrame with a column "Total Sales"
        sales_values = city_sales['Total Sales']  # Extract the sales column directly

    else:
        raise ValueError("city_sales must be a dictionary or a pandas DataFrame.")

    # Create a list to store inertia values for different k values
    inertias = []

    # Range of k values to test (adjust as needed)
    for k in range(1, 11):
        # Create a KMeans instance with k clusters
        kmeans = KMeans(n_clusters=k, random_state=0)

        # Reshape sales_values to a 2D NumPy array (required by KMeans.fit)
        sales_values_array = np.array(sales_values).reshape(-1, 1)

        # Fit KMeans to the reshaped data
        kmeans.fit(sales_values_array)

        # Append the inertia (sum of squared distances to cluster centers)
        inertias.append(kmeans.inertia_)

    # Identify the elbow point (where the inertia starts to plateau)

    lowest_change = float('inf')
    optimal_k = 1
    for i in range(1, len(inertias)):
        change = inertias[i - 1] - inertias[i]
        if change < lowest_change:
            lowest_change = change
            optimal_k = i + 1

    # Return the optimal number of tiers
    return optimal_k


def create_sales_tiers():
    city_sales = fetch_and_convert_sales_data()
    optimal_k = determine_optimal_tiers(city_sales)

    # Check if city_sales is a dictionary or DataFrame
    if not isinstance(city_sales, (dict, pd.DataFrame)):
        raise ValueError("city_sales must be a dictionary or a pandas DataFrame.")

    # Extract sales values
    if isinstance(city_sales, dict):
        df = pd.DataFrame.from_dict(city_sales, orient='index', columns=['Total Sales'])
        sales_values = df['Total Sales'].tolist()
    elif isinstance(city_sales, pd.DataFrame):
        sales_values = city_sales['Total Sales']
    else:
        raise ValueError("Unexpected data type for city_sales.")  # More specific error

    # Reshape sales_values to a 2D NumPy array (required by KMeans.fit)
    sales_values_array = np.array(sales_values).reshape(-1, 1)

    # Create a KMeans instance with the optimal k
    kmeans = KMeans(n_clusters=optimal_k, random_state=0)

    # Fit KMeans to the reshaped data
    kmeans.fit(sales_values_array)

    # Assign cluster labels (tier labels) to each city
    tier_labels = kmeans.labels_

    # Create a DataFrame with city names and tier labels
    df_tiers = pd.DataFrame({'City': city_sales.keys(), 'Tier': tier_labels})
    df_tiers.set_index('City', inplace=True)  # Set 'City' as the index

    # Convert DataFrame to JSON format with city names as keys
    json_data = df_tiers.to_dict(orient='index')  # Convert to dictionary with city names as keys

    return json.dumps(json_data)
