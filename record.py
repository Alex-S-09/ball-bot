import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

out = cv2.VideoWriter(f"clip_{int(time.time())}.mp4",
                      cv2.VideoWriter_fourcc(*"mp4v"), 20, (640, 480))
print("recording... Ctrl+C to stop")
try:
    while True:
        ok, frame = cap.read()
        if ok:
            out.write(frame)
except KeyboardInterrupt:
    pass
finally:
    out.release()
    cap.release()
    print("saved")