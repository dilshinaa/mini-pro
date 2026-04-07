import cv2
import threading
import time
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

QUALITY = 60

def apply_quality(frame, quality):
    if quality == 100:
        return frame

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', frame, encode_param)

    if not result:
        return frame

    return cv2.imdecode(encimg, 1)


VIDEO_PATHS = {
    1: "videos/bus1.mp4",
    2: "videos/bus2.mp4",
    3: "videos/bus3.mp4"
}

bus_data = {1: {}, 2: {}, 3: {}}
latest_frames = {1: None, 2: None, 3: None}
last_processed_frames = {1: None, 2: None, 3: None}


SEAT_POSITIONS = {
    1: [(50,100,150,200),(160,100,260,200),(270,100,370,200)],

    2: [
        (60,130,110,200),
        (115,130,165,200),
        (170,130,220,200),
        (225,130,275,200),
        (280,130,330,200),
        (340,140,390,220),
        (400,140,450,220)
    ],

    3: [(70,130,170,230),(190,130,290,230),(310,130,410,230)]
}


# 🔥 IoU FUNCTION
def compute_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1g, y1g, x2g, y2g = box2

    xi1 = max(x1, x1g)
    yi1 = max(y1, y1g)
    xi2 = min(x2, x2g)
    yi2 = min(y2, y2g)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    union_area = (x2-x1)*(y2-y1) + (x2g-x1g)*(y2g-y1g) - inter_area

    return inter_area / union_area if union_area > 0 else 0


def process_video(bus_id):

    cap = cv2.VideoCapture(VIDEO_PATHS[bus_id])

    prev_passengers = 0
    frame_count = 0

    bus_data[bus_id] = {
        "passengers": 0,
        "available": len(SEAT_POSITIONS[bus_id]),
        "crowd": "Low",
        "occupancy": 0
    }

    while True:

        ret, frame = cap.read()

        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame = cv2.resize(frame, (416, 320))

        # ✅ ONLY CHANGE HERE
        if bus_id == 2:
            frame = apply_quality(frame, 34)
        else:
            frame = apply_quality(frame, QUALITY)

        frame_count += 1

        if frame_count % 2 != 0:
            if last_processed_frames[bus_id] is not None:
                latest_frames[bus_id] = last_processed_frames[bus_id]
            continue

        start_time = time.time()

        try:
            results = model(frame)
        except:
            continue

        fps = 1 / (time.time() - start_time)

        person_boxes = []

        for r in results:
            for box in r.boxes:

                if int(box.cls[0]) == 0 and float(box.conf[0]) > 0.25:

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    person_boxes.append((x1, y1, x2, y2))

        filtered_boxes = []

        for box in person_boxes:
            keep = True

            for fbox in filtered_boxes:
                if compute_iou(box, fbox) > 0.7:
                    keep = False
                    break

            if keep:
                filtered_boxes.append(box)

        person_boxes = filtered_boxes
        passengers = len(person_boxes)

        passengers = max(passengers, int(prev_passengers * 0.9))
        prev_passengers = passengers

        for (x1, y1, x2, y2) in person_boxes:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        seat_regions = SEAT_POSITIONS[bus_id]
        total_seats = len(seat_regions)

        occupied_seats = 0

        for seat in seat_regions:
            sx1, sy1, sx2, sy2 = seat
            occupied = False

            for (x1, y1, x2, y2) in person_boxes:

                overlap_x1 = max(sx1, x1)
                overlap_y1 = max(sy1, y1)
                overlap_x2 = min(sx2, x2)
                overlap_y2 = min(sy2, y2)

                overlap_area = max(0, overlap_x2 - overlap_x1) * max(0, overlap_y2 - overlap_y1)
                person_area = (x2 - x1) * (y2 - y1)

                if person_area > 0 and (overlap_area / person_area) > 0.2:
                    occupied = True
                    break

            if occupied:
                occupied_seats += 1
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)

            cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), color, 2)

        occupied_seats = min(occupied_seats, total_seats)
        available = total_seats - occupied_seats

        seat_ratio = occupied_seats / total_seats if total_seats > 0 else 0
        passenger_ratio = passengers / (total_seats + 2)

        if seat_ratio < 0.3:
            occupancy = passenger_ratio
        else:
            occupancy = max(seat_ratio, passenger_ratio)

        if occupancy < 0.80:
            crowd = "Low"
        elif occupancy < 0.75:
            crowd = "Medium"
        elif occupancy < 0.8:
            crowd = "High"
        else:
            crowd = "Overcrowded"

        cv2.putText(frame, f"Passengers: {passengers}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        cv2.putText(frame, f"Available Seats: {available}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2)

        cv2.putText(frame, f"Crowd: {crowd}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        cv2.putText(frame, f"Occupancy: {occupancy*100:.1f}%", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)

        bus_data[bus_id] = {
            "passengers": passengers,
            "available": available,
            "crowd": crowd,
            "occupancy": round(occupancy * 100, 2)
        }

        last_processed_frames[bus_id] = frame
        latest_frames[bus_id] = frame


def start_ai_detection():
    for bus_id in VIDEO_PATHS:
        thread = threading.Thread(target=process_video, args=(bus_id,))
        thread.daemon = True
        thread.start()


def get_bus_data(bus_id):
    return bus_data.get(bus_id, {
        "passengers": 0,
        "available": 0,
        "crowd": "Low",
        "occupancy": 0
    })


def get_frame(bus_id):

    frame = latest_frames.get(bus_id)

    if frame is None:
        return None

    ret, buffer = cv2.imencode('.jpg', frame)

    if not ret:
        return None

    return buffer.tobytes()