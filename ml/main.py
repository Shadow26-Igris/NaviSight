import cv2
import time
import numpy as np
from datetime import datetime
from ml.detection import ObjectDetector
from ml.tts import TextToSpeech
from ml.voice_command import VoiceCommand
from ml.scene_segmentation import SceneSegmenter

# Global variable for storing the latest alert message
latest_alert = ""

# Function to get the latest alert
def get_latest_alert():
    return latest_alert

# Function to log events with timestamp
def log_event(message, log_file="detection_log.txt"):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} {message}\n")

# Main generator function to process video feed, detect objects, and provide alerts
def main_generator():
    # Initialize models and services
    detector = ObjectDetector()
    tts = TextToSpeech()
    voice_cmd = VoiceCommand()
    segmenter = SceneSegmenter()

    # Variables for handling alerts and frame processing
    last_alert = ""
    alert_cooldown = 5
    last_alert_time = 0
    frame_skip = 2
    frame_count = 0

    # Start video capture (webcam)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return

    # Initial startup announcement
    tts.speak("NaviAid started. Streaming mode enabled.")
    global latest_alert
    latest_alert = "NaviAid started. Streaming mode enabled."
    log_event("System started")

    while True:
        # Capture the current frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        frame = cv2.resize(frame, (640, 480))  # Resize frame to a manageable size
        frame_width = frame.shape[1]

        # Time tracking for alert cool-down
        current_time = time.time()
        alert_text = ""
        detected_objects_this_frame = []

        # Object detection
        frame_with_boxes, results = detector.detect(frame)
        CONFIDENCE_THRESHOLD = 0.4
        navigational_objects = ['person', 'car', 'bus', 'truck', 'bicycle', 'motorcycle']
        obstacle_objects = ['chair', 'bench', 'pole', 'fire hydrant', 'potted plant']
        relevant_objects = navigational_objects + obstacle_objects

        for detection in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = detection
            if conf < CONFIDENCE_THRESHOLD:
                continue

            label = detector.model.names[int(cls)]
            if label in relevant_objects:
                width = x2 - x1
                height = y2 - y1
                box_area = width * height

                if box_area < 25000:
                    continue

                center_x = (x1 + x2) / 2
                if center_x < frame_width / 3:
                    direction = "on the left"
                elif center_x > frame_width * 2 / 3:
                    direction = "on the right"
                else:
                    direction = "ahead"

                label_with_direction = f"a {label} {direction}"
                detected_objects_this_frame.append(label_with_direction)

                alert_text = f"{label} {direction}"
                if alert_text != last_alert or (current_time - last_alert_time) > alert_cooldown:
                    print(alert_text)
                    tts.speak(alert_text)
                    latest_alert = alert_text
                    log_event(f"YOLO - {alert_text} (conf: {conf:.2f})")
                    last_alert = alert_text
                    last_alert_time = current_time
                    break

        # Scene segmentation for walls and stairs
        seg_mask = segmenter.segment(frame)
        labels_detected = segmenter.get_detected_labels(seg_mask)

        for label, count in labels_detected.items():
            if label == "wall" and count > 10000:
                wall_mask = (seg_mask == 0).astype('uint8') * 255
                h, w = wall_mask.shape
                left_half = wall_mask[:, :w // 2]
                right_half = wall_mask[:, w // 2:]
                left_wall_count = np.count_nonzero(left_half)
                right_wall_count = np.count_nonzero(right_half)
                total_wall = left_wall_count + right_wall_count

                if total_wall == 0:
                    continue

                left_ratio = left_wall_count / total_wall
                right_ratio = right_wall_count / total_wall

                if left_ratio > 0.6:
                    tts.speak("Wall on the left.")
                    latest_alert = 'Wall on the left'
                    log_event("Segmentation - Wall on the left")
                    last_alert = "Wall on the left"
                elif right_ratio > 0.6:
                    tts.speak("Wall on the right.")
                    latest_alert = 'Wall on the right'
                    log_event("Segmentation - Wall on the right")
                    last_alert = "Wall on the right"
                else:
                    tts.speak("Wall ahead.")
                    latest_alert = 'Wall ahead'
                    log_event("Segmentation - Wall ahead")
                    last_alert = "Wall ahead"
                last_alert_time = current_time

            elif label == "stairs" and count > 1000:
                stairs_mask = (seg_mask == 53).astype('uint8') * 255
                h, w = stairs_mask.shape
                left_half = stairs_mask[:, :w // 2]
                right_half = stairs_mask[:, w // 2:]
                left_count = np.count_nonzero(left_half)
                right_count = np.count_nonzero(right_half)
                total = left_count + right_count

                if total == 0:
                    continue

                left_ratio = left_count / total
                right_ratio = right_count / total

                if left_ratio > 0.6:
                    tts.speak("Stairs on the left. Be careful.")
                    latest_alert = "Stairs on the left. Be careful."
                    log_event("Segmentation - Stairs on the left")
                    last_alert = "Stairs on the left"
                elif right_ratio > 0.6:
                    tts.speak("Stairs on the right. Be careful.")
                    latest_alert = "Stairs on the right. Be careful."
                    log_event("Segmentation - Stairs on the right")
                    last_alert = "Stairs on the right"
                else:
                    tts.speak("Stairs ahead. Be careful.")
                    latest_alert = 'Stairs ahead. Be careful.'
                    log_event("Segmentation - Stairs ahead")
                    last_alert = "Stairs ahead"
                last_alert_time = current_time

        # Voice trigger: Listen for "What's around me?"
        if frame_count % (frame_skip * 150) == 0:
            tts.speak("Listening for surroundings.")
            latest_alert = 'Listening for surrounding.'
            log_event("Voice: Listening started")
            voice_input = voice_cmd.listen(timeout=2, phrase_time_limit=4)
            if voice_input and "around" in voice_input.lower():
                if detected_objects_this_frame:
                    response = "There is " + ", and ".join(detected_objects_this_frame) + "."
                else:
                    response = "I don't see anything around you clearly."
                tts.speak(response)
                latest_alert = response
                log_event(f"Voice: What's around me? Response: {response}")

        # Frame processing for video streaming
        blended = frame.copy()
        _, buffer = cv2.imencode('.jpg', blended)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Clean up resources after the loop ends
    cap.release()
    log_event("System shutdown")
    cv2.destroyAllWindows()

