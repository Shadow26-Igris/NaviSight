from flask import Blueprint, Response, jsonify
from ml.main import main_generator, get_latest_alert

vision_bp = Blueprint('vision', __name__)

@vision_bp.route('/vision/stream')
def video_stream():
    return Response(main_generator(), mimetype='multipart/x-mixed-replace; boundary=frame')

@vision_bp.route('/vision/alert')
def alert():
    return jsonify({'alert': get_latest_alert()})
