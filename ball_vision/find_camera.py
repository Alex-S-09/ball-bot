import sys
import cv2

BACKEND = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY

for i in range(4):
    cap = cv2.VideoCapture(i, BACKEND)
    if not cap.isOpened():
        print(f"camera {i}: not found")
        continue
    ok, frame = cap.read()
    cap.release()
    if not ok:
        print(f"camera {i}: opened but gave no frame (in use by another app?)")
        continue
    print(f"camera {i} works, frame size {frame.shape[1]}x{frame.shape[0]}")
    cv2.imshow(f"camera {i} (press any key for next)", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()