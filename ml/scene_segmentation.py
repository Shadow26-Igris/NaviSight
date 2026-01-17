import torch
import cv2
import numpy as np
from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation

class SceneSegmenter:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.processor = AutoImageProcessor.from_pretrained("nvidia/segformer-b0-finetuned-ade-512-512")
        self.model = AutoModelForSemanticSegmentation.from_pretrained(
            "nvidia/segformer-b0-finetuned-ade-512-512"
        ).to(self.device).eval()

        self.class_labels = {
            0: "wall",
            3: "floor",
            9: "road",
            20: "sidewalk",
            53: "stairs",
            12: "person"
        }

    def segment(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        inputs = self.processor(images=image_rgb, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        seg = logits.argmax(dim=1)[0].cpu().numpy()
        seg_resized = cv2.resize(seg, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
        return seg_resized

    def get_detected_labels(self, seg_mask):
        labels_detected = {}
        unique_ids = np.unique(seg_mask)
        for class_id in unique_ids:
            if class_id in self.class_labels:
                count = np.count_nonzero(seg_mask == class_id)
                labels_detected[self.class_labels[class_id]] = count
        return labels_detected
