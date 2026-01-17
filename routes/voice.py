from flask import Blueprint, request, send_file, jsonify
from services.tts_service import generate_speech
import os

voice_bp = Blueprint('voice', __name__, url_prefix='/voice')

@voice_bp.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text field is required"}), 400

    try:
        filepath = generate_speech(text)
        return send_file(filepath, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
