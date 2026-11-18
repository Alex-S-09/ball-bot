import sys
import cv2
from vision import find_ball

CAMERA = 0  # use 0 on the pi-top
BACKEND = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY

cap = cv2.VideoCapture(CAMERA, BACKEND)
if not cap.isOpened():
    print(f"Could not open camera {CAMERA} - run find_camera.py to find the number")
    sys.exit(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Running. Hold a ball in front of the camera. Ctrl+C to stop.")
try:
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Camera stopped giving frames")
            break
        print(find_ball(frame))
except KeyboardInterrupt:
    pass
finally:
    cap.release()