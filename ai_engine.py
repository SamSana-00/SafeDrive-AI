import cv2
import mediapipe as mp
import math
import time
import requests
import winsound
from datetime import datetime

# =============================
# BACKEND URL
# =============================
BACKEND_URL = "http://127.0.0.1:8000/log-risk"

# =============================
# SEND TO BACKEND
# =============================
def send_to_backend(duration):

    data = {
        "driver_id": "driver_001",
        "risk_score": 100,
        "eye_duration": duration,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        requests.post(BACKEND_URL, json=data)
        print("Emergency data sent to backend.")
    except:
        print("Backend not reachable")


# =============================
# MediaPipe Setup
# =============================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def calculate_EAR(landmarks, eye_indices, frame_w, frame_h):
    points = []
    for idx in eye_indices:
        x = int(landmarks[idx].x * frame_w)
        y = int(landmarks[idx].y * frame_h)
        points.append((x, y))

    A = math.dist(points[1], points[5])
    B = math.dist(points[2], points[4])
    C = math.dist(points[0], points[3])

    return (A + B) / (2.0 * C)


# =============================
# Calibration Setup
# =============================
calibration_start = time.time()
calibration_duration = 5
baseline_values = []
calibrated = False
EAR_THRESHOLD = 0.25

# =============================
# State Variables
# =============================
state = "CALIBRATING"
eye_closed_start = None
last_open_time = None
emergency_sent = False
last_beep_time = 0
siren_playing = False

OPEN_BUFFER_TIME = 1.5

# =============================
# Start Camera
# =============================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_h, frame_w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            left_EAR = calculate_EAR(face_landmarks.landmark, LEFT_EYE, frame_w, frame_h)
            right_EAR = calculate_EAR(face_landmarks.landmark, RIGHT_EYE, frame_w, frame_h)
            avg_EAR = (left_EAR + right_EAR) / 2

            current_time = time.time()

            # ===== Calibration =====
            if not calibrated:
                if current_time - calibration_start < calibration_duration:
                    baseline_values.append(avg_EAR)
                    cv2.putText(frame, "Calibrating... Keep eyes open",
                                (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 255, 255),
                                2)
                else:
                    baseline_ear = sum(baseline_values) / len(baseline_values)
                    EAR_THRESHOLD = baseline_ear * 0.65
                    calibrated = True
                    print("Calibration Complete. Threshold:", EAR_THRESHOLD)

            # ===== After Calibration =====
            if calibrated:

                if avg_EAR < EAR_THRESHOLD:
                    if eye_closed_start is None:
                        eye_closed_start = current_time
                    last_open_time = None
                else:
                    if last_open_time is None:
                        last_open_time = current_time
                    elif current_time - last_open_time > OPEN_BUFFER_TIME:
                        eye_closed_start = None

                closed_duration = 0
                if eye_closed_start is not None:
                    closed_duration = current_time - eye_closed_start

                # ===== Escalation =====
                if closed_duration > 10:
                    state = "EMERGENCY"
                elif closed_duration > 5:
                    state = "CRITICAL"
                elif closed_duration > 2:
                    state = "WARNING"
                else:
                    state = "NORMAL"

                # ===== Alert System =====
                if state == "NORMAL":
                    color = (0, 255, 0)
                    emergency_sent = False

                    if siren_playing:
                        winsound.PlaySound(None, winsound.SND_PURGE)
                        siren_playing = False

                elif state == "WARNING":
                    color = (0, 165, 255)
                    if current_time - last_beep_time > 2:
                        winsound.Beep(800, 200)
                        last_beep_time = current_time

                elif state == "CRITICAL":
                    color = (0, 0, 255)
                    if current_time - last_beep_time > 1:
                        winsound.Beep(1200, 500)
                        last_beep_time = current_time

                elif state == "EMERGENCY":
                    color = (0, 0, 255)

                    if not siren_playing:
                        winsound.PlaySound(
                            "ambulance.wav",
                            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
                        )
                        siren_playing = True

                    if not emergency_sent:
                        send_to_backend(closed_duration)
                        emergency_sent = True

                # ===== Display =====
                cv2.putText(frame, state, (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                            color, 3)

                cv2.putText(frame, f"EAR: {round(avg_EAR,3)}",
                            (30, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (255,255,255), 2)

                cv2.putText(frame, f"Closed Duration: {round(closed_duration,1)}",
                            (30, 170),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (255,255,255), 2)

    cv2.imshow("SafeDrive AI", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
winsound.PlaySound(None, winsound.SND_PURGE)
cv2.destroyAllWindows()
