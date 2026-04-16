# from object_detection import detect_objects
# from lane_detection import detect_lanes
# from weather import detect_weather
# from sign_detection import detect_signs

# def to_python(obj):
#     if isinstance(obj, dict):
#         return {k: to_python(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [to_python(i) for i in obj]
#     elif isinstance(obj, tuple):
#         return [int(i) for i in obj]  
#     elif hasattr(obj, "item"):  
#         return obj.item()  
#     else:
#         return obj

# def process_frame(frame):
#     objects = detect_objects(frame)
#     lanes = detect_lanes(frame)
#     weather = detect_weather(frame)
#     signs = detect_signs(frame)

#     result = {
#         "objects": objects,
#         "lanes": lanes,
#         "weather": weather,
#         "signs": signs
#     }

#     return to_python(result) 
from object_detection import detect_objects
from lane_detection import detect_lanes
from weather import detect_weather
from sign_detection import detect_signs

def to_python(obj):
    if isinstance(obj, dict):
        return {k: to_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_python(i) for i in obj]
    elif isinstance(obj, tuple):
        return [int(i) for i in obj]
    elif hasattr(obj, "item"):
        return obj.item()
    else:
        return obj


def process_frame(frame):
    objects = detect_objects(frame)

    # ✅ FIX IS HERE
    lanes, lane_detected = detect_lanes(frame)

    weather = detect_weather(frame)
    signs = detect_signs(frame)

    result = {
        "objects": objects,
        "lanes": lanes,
        "lane_detected": lane_detected,
        "weather": weather,
        "signs": signs
    }

    return to_python(result)