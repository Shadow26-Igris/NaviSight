from flask import Blueprint, request, jsonify
from ml.navigation import Navigation
import os

navigation_bp = Blueprint('navigation', __name__)
nav = Navigation(api_key=os.environ.get("GOOGLE_MAPS_API_KEY"))

@navigation_bp.route('/navigate', methods=['POST'])
def navigate():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    if not origin or not destination:
        return jsonify({"error": "Missing origin or destination"}), 400

    success = nav.get_directions(origin, destination)
    return jsonify({"success": success})
