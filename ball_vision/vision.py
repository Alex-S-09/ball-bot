import cv2

PARAM2 = 22     # lower = more detections (and more false ones)
MIN_R = 15      # smallest ball radius in pixels (far away)
MAX_R = 35      # largest radius (ball at the bottom edge of the frame)
CROP_TOP = 0.49  # fraction of the frame to ignore from the top (0 to 0.8)


def find_ball(frame):
    """Returns (x_offset, size, y_frac) or None.

    x_offset: -1 (far left) .. +1 (far right), 0 = centered
    size: ball width as a fraction of the frame width (bigger = closer)
    y_frac: ball center height in the full frame, 0 = top, 1 = bottom
    """
    h, w = frame.shape[:2]
    y0 = int(h * CROP_TOP)
    gray = cv2.cvtColor(frame[y0:], cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=40,
                               param1=100, param2=PARAM2,
                               minRadius=MIN_R, maxRadius=MAX_R)
    if circles is None:
        return None

    x, y, r = max(circles[0], key=lambda c: c[2])  # biggest = closest
    return ((x - w / 2) / (w / 2), (2 * r) / w, (y + y0) / h)