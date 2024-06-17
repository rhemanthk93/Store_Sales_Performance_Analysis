from flask import Blueprint, jsonify
from app.database_queries.sales_insights import get_city_with_per_hour_sales, get_city_with_avg_sales_with_district_info, \
    get_time_based_sales_trend_by_city

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