import cv2
import numpy as np

def road_segmentation(frame):
    """
    Lightweight road + lane segmentation (YOLO-style preprocessing hybrid)
    """

    h, w = frame.shape[:2]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # road color cues (asphalt + lane paint)
    lower_road = np.array([0, 0, 40])
    upper_road = np.array([180, 70, 255])

    road_mask = cv2.inRange(hsv, lower_road, upper_road)

    # lane colors (white/yellow)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 40, 255])

    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    lower_yellow = np.array([15, 80, 80])
    upper_yellow = np.array([40, 255, 255])

    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    lane_mask = cv2.bitwise_or(white_mask, yellow_mask)

    combined = cv2.bitwise_and(road_mask, lane_mask)

    # ROI (road only)
    roi = np.zeros_like(combined)
    polygon = np.array([[
        (0, h),
        (w, h),
        (w, int(h * 0.55)),
        (0, int(h * 0.55))
    ]], np.int32)

    cv2.fillPoly(roi, polygon, 255)

    final_mask = cv2.bitwise_and(combined, roi)

    return final_mask


def extract_lanes(mask):
    edges = cv2.Canny(mask, 50, 150)

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi/180,
        threshold=30,
        minLineLength=25,
        maxLineGap=60
    )

    if lines is None:
        return [], False

    lane_lines = []

    for l in lines:
        x1, y1, x2, y2 = l[0]

        slope = (y2 - y1) / (x2 - x1 + 1e-6)

        # keep only vertical-ish road lanes
        if abs(slope) < 0.5:
            continue

        lane_lines.append([x1, y1, x2, y2])

    return lane_lines[:2], len(lane_lines) > 0


def detect_lanes(frame):
    mask = road_segmentation(frame)
    lanes, detected = extract_lanes(mask)
    return lanes, detected