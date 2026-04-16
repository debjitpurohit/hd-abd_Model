import cv2
import numpy as np

def detect_weather(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contrast = np.std(gray)

    if contrast < 30:
        return "fog"
    elif contrast < 50:
        return "rain"
    return "clear"