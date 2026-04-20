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
from concurrent.futures import ThreadPoolExecutor

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
    with ThreadPoolExecutor() as executor:
        # run all tasks in parallel
        obj_future = executor.submit(detect_objects, frame)
        lane_future = executor.submit(detect_lanes, frame)
        weather_future = executor.submit(detect_weather, frame)
        sign_future = executor.submit(detect_signs, frame)

        # collect results
        objects = obj_future.result()
        lanes, lane_detected = lane_future.result()
        weather = weather_future.result()
        signs = sign_future.result()

    result = {
        "objects": objects,
        "lanes": lanes,
        "lane_detected": lane_detected,
        "weather": weather,
        "signs": signs
    }

    return to_python(result)
