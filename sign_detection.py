import cv2
import numpy as np

def detect_signs(frame):
    # 1. Blur to reduce noise and sharp glare
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)

    # 2. Convert to HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # 3. Improved mask (avoid flashlight white glare)
    lower = np.array([0, 40, 180])   # increased saturation threshold
    upper = np.array([180, 150, 255])

    mask = cv2.inRange(hsv, lower, upper)

    # 4. Morphological operations (clean noise)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 5. Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    signs = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # 6. Filter small reflections (flashlight spots)
        if area > 2000:
            x, y, w, h = cv2.boundingRect(cnt)

            # Optional: filter weird shapes
            aspect_ratio = w / float(h)
            if 0.5 < aspect_ratio < 2.0:
                signs.append({
                    "x": int(x),
                    "y": int(y),
                    "w": int(w),
                    "h": int(h)
                })

    return signs
