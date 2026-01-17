from flask import Blueprint, request, jsonify
from geopy.distance import geodesic

route_bp = Blueprint('route', __name__, url_prefix='/route')

@route_bp.route('/get-directions', methods=['POST'])
def get_directions():
    data = request.get_json()
    try:
        user_lat = float(data.get('user_lat'))
        user_lng = float(data.get('user_lng'))
        destination_lat = float(data.get('destination_lat'))
        destination_lng = float(data.get('destination_lng'))

        user_coords = (user_lat, user_lng)
        destination_coords = (destination_lat, destination_lng)
        distance = geodesic(user_coords, destination_coords).km

        return jsonify({"distance": distance})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
