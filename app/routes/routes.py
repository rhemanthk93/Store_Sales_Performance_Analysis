from flask import Blueprint, jsonify
from app.database_queries.sales_insights import get_city_with_per_hour_sales, \
    get_city_with_avg_sales_with_district_info, \
    get_time_based_sales_trend_by_city
from app.database_queries.tier_based_insights import create_sales_tiers
from app.database_queries.order_insights import get_time_based_order_trend_by_city, get_orders_by_region

main = Blueprint('main', __name__)


@main.route('/city_per_hour_sales', methods=['GET'])
def highest_per_hour_sales_by_city():
    try:
        result = get_city_with_per_hour_sales()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/city_avg_sales_with_district', methods=['GET'])
def highest_avg_sales_by_city():
    try:
        result = get_city_with_avg_sales_with_district_info()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/time_based_sales_trend_by_city', methods=['GET'])
def time_based_sales_trend_by_city():
    try:
        result = get_time_based_sales_trend_by_city()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/time_based_order_trend_by_city', methods=['GET'])
def time_based_order_trend_by_city():
    try:
        result = get_time_based_order_trend_by_city()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/orders_by_region', methods=['GET'])
def orders_by_region():
    try:
        result = get_orders_by_region()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/sales_tiers', methods=['GET'])
def get_sales_tiers():
    try:
        result = create_sales_tiers()
        return result
    except Exception as e:
        return jsonify({"error": str(e)}), 500
