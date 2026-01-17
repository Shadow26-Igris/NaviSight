import torch
import cv2

class ObjectDetector:
    def __init__(self, model_name='yolov5s', device=None):
        """
        Initialize the YOLOv5 model for detection.
        model_name: YOLOv5 model variant
        device: 'cpu' or 'cuda', if None will auto-select
        """
        self.device = device if device else ('cuda' if torch.cuda.is_available() else 'cpu')
        # Load model from PyTorch Hub
        self.model = torch.hub.load('ultralytics/yolov5', model_name, pretrained=True)
        self.model.to(self.device)
        self.model.eval()
    
    def detect(self, frame):
        """
        Perform object detection on a frame.
        Returns processed frame with boxes and the raw results tensor.
        """
        results = self.model(frame)
        # results.print()  # Uncomment for debug output to console
        detected_frame = results.render()[0]  # annotated frame as np.array
        return detected_frame, results


if __name__ == "__main__":
    # Simple test to verify the detector works
    cap = cv2.VideoCapture(0)
    detector = ObjectDetector()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_with_boxes, results = detector.detect(frame)
        cv2.imshow("YOLOv5 Detection", frame_with_boxes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
