from flask import Blueprint, jsonify
from app.database_queries.sales_insights import get_city_with_highest_per_hour_sales, get_city_with_highest_avg_sales, \
    get_time_based_sales_trend, get_top_sales_by_region
from app.database_queries.order_insights import get_time_based_order_trend, get_top_orders_by_region
from app.database_queries.tier_based_insights import create_sales_tiers, create_order_frequency_tiers, \
    create_currency_based_tiers, create_peak_hour_tiers

main = Blueprint('main', __name__)


@main.route('/highest_per_hour_sales_by_city', methods=['GET'])
def highest_per_hour_sales_by_city():
    try:
        result = get_city_with_highest_per_hour_sales()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/highest_avg_sales_by_city', methods=['GET'])
def highest_avg_sales_by_city():
    try:
        result = get_city_with_highest_avg_sales()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/time_based_sales_trend', methods=['GET'])
def time_based_sales_trend():
    try:
        result = get_time_based_sales_trend()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/top_sales_by_region', methods=['GET'])
def top_sales_by_region():
    try:
        result = get_top_sales_by_region()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/time_based_order_trend', methods=['GET'])
def time_based_order_trend():
    try:
        result = get_time_based_order_trend()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/top_orders_by_region', methods=['GET'])
def top_orders_by_region():
    try:
        result = get_top_orders_by_region()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/sales_tiers', methods=['GET'])
def get_sales_tiers():
    try:
        sales_tiers_json = create_sales_tiers()
        return jsonify(sales_tiers_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/order_frequency_tiers', methods=['GET'])
def get_order_frequency_tiers():
    try:
        order_frequency_tiers_json = create_order_frequency_tiers()
        return jsonify(order_frequency_tiers_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/currency_tiers', methods=['GET'])
def get_currency_tiers():
    try:
        currency_tiers_json = create_currency_based_tiers()
        return jsonify(currency_tiers_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/peak_hour_tiers', methods=['GET'])
def get_peak_hour_tiers():
    try:
        peak_hour_tiers_json = create_peak_hour_tiers()
        return jsonify(peak_hour_tiers_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
