from flask import Blueprint, jsonify
from app.database_queries.insights import get_city_with_highest_per_hour_sales, get_city_with_highest_avg_sales

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
