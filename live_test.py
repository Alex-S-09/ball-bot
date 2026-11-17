import time
import cv2
from ball_vision.vision import find_ball

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # avoid processing stale frames

n, t0 = 0, time.time()
try:
    while True:
        ok, frame = cap.read()
        if not ok:
            continue
        print(find_ball(frame))
        n += 1
        if n % 30 == 0:
            print(f"--- {n / (time.time() - t0):.1f} fps ---")
except KeyboardInterrupt:
    pass
finally:
    cap.release()