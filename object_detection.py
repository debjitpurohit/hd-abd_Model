from ultralytics import YOLO
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

model = YOLO("yolov8s.pt")

# 🔥 FORCE model to GPU
model.to(device)

# 🔍 Verify
print("Model running on:", next(model.model.parameters()).device)


IMPORTANT_CLASSES = [
    "car", "truck", "bus",
    "person",
    "bicycle", "motorcycle",
    "traffic light", "stop sign",
    "dog", "cat", "cow", "horse", "sheep"
]

def detect_objects(frame):
    print("YOLO CALLED") 

    results = model(frame)   

    objects = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label not in IMPORTANT_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            objects.append({
                "label": label,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            })

    return objects
