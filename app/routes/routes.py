from flask import Blueprint, jsonify
from app.database_queries.sales_insights import get_city_with_highest_per_hour_sales, get_city_with_highest_avg_sales
from app.database_queries.tier_based_insights import create_sales_tiers

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


@main.route('/sales_tiers', methods=['GET'])
def get_sales_tiers():
    try:
        sales_tiers_json = create_sales_tiers()
        return jsonify(sales_tiers_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
