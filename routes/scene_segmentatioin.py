from flask import Blueprint, request, jsonify
import cv2
import numpy as np
import base64
from ml.scene_segmentation import SceneSegmenter

scene_bp = Blueprint('scene', __name__)
segmenter = SceneSegmenter()

@scene_bp.route('/segment-scene', methods=['POST'])
def segment_scene():
    data = request.json
    image_b64 = data.get('image')
    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    # Decode base64 image
    image_data = base64.b64decode(image_b64)
    np_arr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    mask = segmenter.segment(frame)
    labels = segmenter.get_detected_labels(mask)
    return jsonify(labels)
