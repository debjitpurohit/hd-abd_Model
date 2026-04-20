# from ultralytics import YOLO

# model = YOLO("yolov8s.pt")  # lightweight

# def detect_objects(frame):
#     results = model(frame)

#     objects = []
#     for r in results:
#         for box in r.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cx = int((x1 + x2)) // 2
#             cy = int((y1 + y2)) // 2

#             objects.append({"x": cx, "y": cy})

#     return objects
# from ultralytics import YOLO

# model = YOLO("yolov8s.pt")  


# IMPORTANT_CLASSES = [
#     "car", "truck", "bus",
#     "person",
#     "bicycle", "motorcycle",
#     "traffic light"
# ]

# def detect_objects(frame):
#     results = model(frame)

#     objects = []

#     for r in results:
#         for box in r.boxes:
#             cls_id = int(box.cls[0])
#             label = model.names[cls_id]

            
#             if label not in IMPORTANT_CLASSES:
#                 continue

#             x1, y1, x2, y2 = map(int, box.xyxy[0])

#             cx = int((x1 + x2)) // 2
#             cy = int((y1 + y2)) // 2

#             objects.append({
#                 "x": cx,
#                 "y": cy,
#                 "label": label
#             })

#     return objects
from ultralytics import YOLO
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO("yolov8s.pt").to(device)
print(torch.cuda.is_available())

# model = YOLO("yolov8s.pt")

IMPORTANT_CLASSES = [
    "car", "truck", "bus",
    "person",
    "bicycle", "motorcycle",
    "traffic light", "stop sign","dog", "cat", "cow", "horse", "sheep"
]

def detect_objects(frame):
    results = model(frame,device=0)

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
