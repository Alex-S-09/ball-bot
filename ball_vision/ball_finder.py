import sys
import time
import cv2
from vision import find_ball

BACKEND = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY


class BallFinder:
    """Tells you when a ball is found.

    found = BallFinder(camera=0).update()   # call once per loop
    """

    def __init__(self, camera=0, frames_required=3, lost_timeout=0.5):
        self.cap = cv2.VideoCapture(camera, BACKEND)
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera {camera}")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # must match the tuning size
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.frames_required = frames_required  # detections in a row to count as "found"
        self.lost_timeout = lost_timeout        # seconds without a ball before "lost"
        self.hits = 0
        self.found = False
        self.last = None        # (x_offset, size, y_frac) of the latest detection
        self.last_seen = 0.0

    def update(self):
        """Read one frame and return True if a ball is currently found."""
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Camera stopped giving frames")

        det = find_ball(frame)
        now = time.time()
        if det:
            self.hits += 1
            self.last, self.last_seen = det, now
            if self.hits >= self.frames_required:
                self.found = True
        else:
            self.hits = 0
            if now - self.last_seen > self.lost_timeout:
                self.found = False
                self.last = None
        return self.found

    def close(self):
        self.cap.release()


PRINT_EVERY_S = 2.0   # how often to print a status line

if __name__ == "__main__":
    camera = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    finder = BallFinder(camera)
    next_print = 0.0
    print("Watching for a ball. Ctrl+C to stop.")
    try:
        while True:
            found = finder.update()
            now = time.time()
            if now >= next_print:
                if found:
                    x, size, y = finder.last
                    print(f"BALL FOUND  x_offset={x:+.2f}  size={size:.3f}  y_frac={y:.2f}")
                else:
                    print("no ball")
                next_print = now + PRINT_EVERY_S
    except KeyboardInterrupt:
        pass
    finally:
        finder.close()