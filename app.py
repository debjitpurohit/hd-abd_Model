from flask import Flask, request, jsonify
import cv2
import numpy as np
from pipeline import process_frame
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/detect": {
    "origins": "https://car-display-interface--aececedebjitpur.replit.app"
}})

# ✅ STORE LAST RESULT
latest_result = {
    "objects": [],
    "lanes": [],
    "lane_detected": False,
    "weather": "clear"
}

@app.route("/detect", methods=["POST"])
def detect():
    global latest_result
    try:
        file = request.files["image"]

        img_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        result = process_frame(frame)
        print("Result",result);

        # 🔥 SAVE RESULT
        latest_result = result
        print("Latest_Res",latest_result);

        return jsonify(result)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

# ✅ NEW API FOR PI
@app.route("/data", methods=["GET"])
def data():
    return jsonify(latest_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
