# Store Sales Performance Analysis

## Overview

This project is designed to analyze store sales performance across different locations. The application provides insights into sales trends, order timings, and sales distributions, leveraging clustering techniques for deeper analysis.

## Features

- Analysis of store sales performance across different cities.
- Clustering of cities based on sales performance.
- Time-based sales trend analysis.
- Order timing clustering.
- Visualization of sales data using various charts.
- Conversion of Exhange Rates between usd and rmb
- Translation of chinese to english using google trans

# Store Sales Performance Analysis - Dependencies

This document lists all the dependencies required to run the Store Sales Performance Analysis Flask application.

## Python Dependencies

- **Flask**: A micro web framework for Python. Used for developing the web application.
  - Installation: `pip install Flask`
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python. Used for database interactions.
  - Installation: `pip install SQLAlchemy`
- **pandas**: A powerful data analysis and manipulation library for Python.
  - Installation: `pip install pandas`
- **scikit-learn**: A machine learning library for Python. Used for clustering algorithms.
  - Installation: `pip install scikit-learn`
- **kneed**: A library to detect the knee/elbow point in a curve. Used to determine the optimal number of clusters.
  - Installation: `pip install kneed`
- **matplotlib**: A plotting library for Python. Used for data visualization.
  - Installation: `pip install matplotlib`
- **PyMySQL**: A pure-Python MySQL client library. Used for connecting to a MySQL database.
  - Installation: `pip install PyMySQL`

## Other Dependencies

- **MySQL Server**: The database server where the data is stored.
  - Installation: Follow the instructions on the [official MySQL website](https://dev.mysql.com/doc/refman/8.0/en/installing.html).

## Development and Testing Tools

- **pytest**: A framework for testing Python code.
  - Installation: `pip install pytest`
- **pytest-flask**: A set of pytest fixtures to test Flask applications.
  - Installation: `pip install pytest-flask`

## Installation Instructions

1. **Clone the Repository**: 
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**:
    - Ensure MySQL Server is installed and running.
    - Create a database for the project.
    - Update the database configuration in the Flask application (usually in `config.py` or similar).

5. **Load Data into the Database**:
    - Run the data loading script provided in the project to populate the database with initial data.
    - Example:
      ```bash
      python load_data.py
      ```

6. **Run the Application**:
    ```bash
    flask run
    ```

## Notes

- Ensure that the MySQL server is properly configured and accessible.
- The database schema and initial data loading scripts should be executed before running the application.
- If there are any issues with dependencies, refer to the official documentation of each library for troubleshooting.


# Store Sales Performance Analysis - API Endpoints

This document lists all the API endpoints available in the Store Sales Performance Analysis Flask application.

## Endpoints

### 1. `/city_per_hour_sales`
- **Method:** GET
- **Description:** Retrieves the highest per-hour sales data for each city.
- **Response:** JSON with city and sales data.

### 2. `/city_avg_sales_with_district`
- **Method:** GET
- **Description:** Retrieves the average sales data for each city along with district information.
- **Response:** JSON with city, average sales, and district information.

### 3. `/time_based_sales_trend_by_city`
- **Method:** GET
- **Description:** Retrieves the time-based sales trend data for each city.
- **Response:** JSON with city and sales trend data.

### 4. `/time_based_order_trend_by_city`
- **Method:** GET
- **Description:** Retrieves the time-based order trend data for each city.
- **Response:** JSON with city and order trend data.

### 5. `/orders_by_region`
- **Method:** GET
- **Description:** Retrieves the number of orders by region.
- **Response:** JSON with region and order count data.

### 6. `/sales_tiers`
- **Method:** GET
- **Description:** Retrieves sales tier data based on sales performance.
- **Response:** JSON with city and sales tier data.

### 7. `/order_timing_tiers`
- **Method:** GET
- **Description:** Retrieves order timing clustering data.
- **Response:** JSON with order timing clustering data.

### 8. `/orders_by_city_currency`
- **Method:** GET
- **Description:** Retrieves the number of orders by city and currency (USD or RMB).
- **Response:** JSON with city, currency, and order count data.

## Notes

- Each endpoint returns data in JSON format.
- In case of an error, the endpoints return a JSON response with an error message and a 500 status code.
- Ensure that the database is properly configured and the required data is loaded before accessing these endpoints.

