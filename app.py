# # from flask import Flask, request, jsonify
# # import cv2
# # import numpy as np
# # from pipeline import process_frame

# # app = Flask(__name__)

# # @app.route("/detect", methods=["POST"])
# # def detect():
# #     try:
# #         file = request.files["image"]

# #         img_bytes = np.frombuffer(file.read(), np.uint8)
# #         frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

# #         frame = cv2.resize(frame, (320, 240))

# #         result = process_frame(frame)

# #         return jsonify(result)

# #     except Exception as e:
# #         print(" ERROR:", e)
# #         return jsonify({"error": str(e)}), 500

# # if __name__ == "__main__":
# #     app.run(debug=True)

from flask import Flask, request, jsonify
import cv2
import numpy as np
from pipeline import process_frame
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/detect": {
    "origins": "https://car-display-interface--aececedebjitpur.replit.app"
}})
@app.route("/detect", methods=["POST"])
def detect():
    try:
        file = request.files["image"]

        img_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        result = process_frame(frame)

        return jsonify(result)

    except Exception as e:
        print(" ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
# import cv2
# import numpy as np
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# from aiortc import RTCPeerConnection, RTCSessionDescription
# from aiortc.contrib.media import MediaBlackhole

# from pipeline import process_frame

# app = Flask(__name__)
# CORS(app)

# pcs = set()


# # -------------------------------
# # WebRTC Peer Connection
# # -------------------------------
# @app.route("/offer", methods=["POST"])
# async def offer():
#     params = request.json
#     offer = RTCSessionDescription(
#         sdp=params["sdp"],
#         type=params["type"]
#     )

#     pc = RTCPeerConnection()
#     pcs.add(pc)

#     @pc.on("track")
#     def on_track(track):

#         print("Track received:", track.kind)

#         if track.kind == "video":

#             async def process_video():
#                 while True:
#                     frame = await track.recv()

#                     img = frame.to_ndarray(format="bgr24")

#                     result = process_frame(img)

#                     # You can store or broadcast result later
#                     print(result)

#             import asyncio
#             asyncio.create_task(process_video())

#     await pc.setRemoteDescription(offer)

#     answer = await pc.createAnswer()
#     await pc.setLocalDescription(answer)

#     return jsonify({
#         "sdp": pc.localDescription.sdp,
#         "type": pc.localDescription.type
#     })


# # -------------------------------
# # OPTIONAL: fallback API
# # -------------------------------
# @app.route("/detect", methods=["POST"])
# def detect():
#     file = request.files["image"]
#     npimg = np.frombuffer(file.read(), np.uint8)
#     frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

#     return jsonify(process_frame(frame))


# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
