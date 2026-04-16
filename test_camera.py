import cv2
import requests
import time

URL = "http://127.0.0.1:5000/detect"

cap = cv2.VideoCapture(0)
start_time = time.time()

# 🔥 8x8 MATRIX
def matrix_glare_control(objects, width, height):
    rows, cols = 8, 8
    matrix = [["HIGH" for _ in range(cols)] for _ in range(rows)]

    cell_w = width // cols
    cell_h = height // rows

    for obj in objects:
        if "x1" not in obj:
            continue

        label = obj["label"]

        if label not in ["car", "person", "bicycle", "motorcycle"]:
            continue

        x1, y1 = obj["x1"], obj["y1"]
        x2, y2 = obj["x2"], obj["y2"]

        col_start = max(0, min(cols-1, x1 // cell_w))
        col_end   = max(0, min(cols-1, x2 // cell_w))
        row_start = max(0, min(rows-1, y1 // cell_h))
        row_end   = max(0, min(rows-1, y2 // cell_h))

        for r in range(row_start, row_end + 1):
            for c in range(col_start, col_end + 1):
                matrix[r][c] = "LOW"

    return matrix


# 🔥 DRAW MATRIX WITH TEXT
def draw_matrix(frame, matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    h, w, _ = frame.shape

    cell_w = w // cols
    cell_h = h // rows

    for i in range(rows):
        for j in range(cols):
            x1 = j * cell_w
            y1 = i * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h

            state = matrix[i][j]

            if state == "LOW":
                overlay = frame.copy()
                cv2.rectangle(overlay, (x1,y1), (x2,y2), (0,0,255), -1)
                cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)
                color = (0,0,255)
            else:
                color = (0,255,0)

            cv2.rectangle(frame, (x1,y1), (x2,y2), color, 1)

            # 🔥 TEXT INSIDE EACH CELL
            cv2.putText(frame,
                        state,
                        (x1 + 5, y1 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,
                        color,
                        1)


while True:

    if time.time() - start_time >50:
        print("⏹️ Done")
        break

    ret, frame = cap.read()
    if not ret:
        break

    # 🔥 BIG SCREEN
    frame = cv2.resize(frame, (960, 720))

    _, img = cv2.imencode('.jpg', frame)

    try:
        response = requests.post(
            URL,
            files={"image": ("frame.jpg", img.tobytes(), "image/jpeg")},
            timeout=5
        )

        data = response.json()

        # 🔴 OBJECTS
        for obj in data["objects"]:
            if "x1" not in obj:
                continue

            x1, y1 = obj["x1"], obj["y1"]
            x2, y2 = obj["x2"], obj["y2"]
            label = obj["label"]

            cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2)
            cv2.putText(frame, label.upper(),
                        (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255,0,0),
                        2)

        # 🟢 LANES
        for i, lane in enumerate(data["lanes"]):
                 x1, y1, x2, y2 = lane

                 color = (255,0,0) if i == 0 else (0,255,0)

                 cv2.line(frame, (x1,y1), (x2,y2), color, 5)
        

        # 🌦 WEATHER
        cv2.putText(frame,
                    "Weather: " + data["weather"],
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2)

        # 💡 TITLE
        cv2.putText(frame,
                    "HD-ADB MATRIX SYSTEM",
                    (300, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (255,255,255),
                    2)

        # 💡 MATRIX
        matrix = matrix_glare_control(
            data["objects"],
            frame.shape[1],
            frame.shape[0]
        )

        draw_matrix(frame, matrix)

    except Exception as e:
        print("Error:", e)

    # cv2.imshow("HD-ADB FINAL SYSTEM", frame)

    # if cv2.waitKey(1) == 27:
    #     break

    time.sleep(0.2)

cap.release()
# cv2.destroyAllWindows()