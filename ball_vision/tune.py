import sys
import cv2
import numpy as np

CAMERA = 0  # camera number used when no argument is given (use 0 on the pi-top)
BACKEND = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY

# Usage:
#   py -3.13 tune.py              -> live camera (CAMERA above)
#   py -3.13 tune.py 0            -> live camera number 0
#   py -3.13 tune.py clip_123.mp4 -> recorded clip
#
# Keys (click the video window first):
#   p = print the radii of the circles in the current frame
#   q = print your four settings and quit
arg = sys.argv[1] if len(sys.argv) > 1 else CAMERA
try:
    src = int(arg)
except ValueError:
    src = arg  # a file path

if isinstance(src, int):
    cap = cv2.VideoCapture(src, BACKEND)
else:
    cap = cv2.VideoCapture(src)

if not cap.isOpened():
    print(f"Could not open camera/video: {src}")
    print("Run find_camera.py to find the right camera number.")
    sys.exit(1)

cv2.namedWindow("tune")
cv2.createTrackbar("param2", "tune", 30, 100, lambda v: None)
cv2.createTrackbar("minR", "tune", 8, 100, lambda v: None)
cv2.createTrackbar("maxR", "tune", 120, 300, lambda v: None)
cv2.createTrackbar("crop_top%", "tune", 0, 80, lambda v: None)

while True:
    ok, frame = cap.read()
    if not ok:
        if isinstance(src, int):
            print("Camera stopped giving frames")
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop the clip
        continue

    p2 = max(1, cv2.getTrackbarPos("param2", "tune"))
    minr = cv2.getTrackbarPos("minR", "tune")
    maxr = max(minr + 1, cv2.getTrackbarPos("maxR", "tune"))
    crop = cv2.getTrackbarPos("crop_top%", "tune") / 100

    h = frame.shape[0]
    y0 = int(h * crop)
    gray = cv2.medianBlur(cv2.cvtColor(frame[y0:], cv2.COLOR_BGR2GRAY), 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40,
                               param1=100, param2=p2,
                               minRadius=minr, maxRadius=maxr)

    if circles is not None:
        for x, y, r in np.round(circles[0]).astype(int):
            cv2.circle(frame, (x, y + y0), r, (0, 255, 0), 2)
            cv2.putText(frame, f"r={r}", (x - 20, y + y0 - r - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.line(frame, (0, y0), (frame.shape[1], y0), (0, 0, 255), 1)  # crop line

    # Fixed readout in the corner: radius of every circle currently detected
    if circles is not None:
        radii = [int(r) for r in np.round(circles[0][:, 2])]
        cv2.putText(frame, f"radii: {radii}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("tune", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord("p"):
        if circles is None:
            print("no circles in this frame")
        else:
            radii = [int(r) for r in np.round(circles[0][:, 2])]
            print("radii (px):", radii)
    elif key == ord("q"):
        print(f"PARAM2={p2}  MIN_R={minr}  MAX_R={maxr}  CROP_TOP={crop:.2f}")
        break

cap.release()
cv2.destroyAllWindows()