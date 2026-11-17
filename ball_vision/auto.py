"""Autonomous ball pickup: search -> approach -> blind drive -> (shoot).

Run on the pi-top:           python3 auto.py
Dry run on the laptop:       py -3.13 auto.py --dry --camera 1
  (--dry prints motor commands instead of moving anything)
"""
import os
import sys
import time

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(_here)
sys.path.append(os.path.join(_here, "ball_vision"))

import cv2
from vision import find_ball

# ---------------------------------------------------------------- CONSTANTS --
CAMERA = 0                 # 0 on the pi-top; use --camera N to override

APPROACH_POWER = 0.35      # forward speed while approaching
SEARCH_TURN = 0.30         # turn-in-place speed while searching
TURN_GAIN = 0.5            # steering strength vs x_offset
MIN_TURN = 0.20            # below this the wheels may not move at all
MAX_TURN = 0.40
ALIGN_TOL = 0.25           # far away: pivot in place if |x_offset| is bigger
ALIGN_TOL_NEAR = 0.08      # close: align much more tightly (no steering later)
NEAR_Y = 0.60              # y_frac above which "near" tolerance applies

DETECT_FRAMES = 3          # detections in a row before the robot trusts a ball
LOST_TIMEOUT = 0.5         # seconds without a ball before giving up and searching

HANDOFF_Y = 0.80           # last seen below this line in the frame, then vanished
HANDOFF_SIZE = 0.056       # about radius 18 px (size = 2 * r / 640)

BLIND_INCHES = 26          # measured: ball at bottom edge -> inside intake
INCHES_PER_SEC = 12.0      # PLACEHOLDER: measure with calibrate_drive.py
BLIND_SETTLE_S = 0.5       # let the ball ride up the ramp

BALLS_PER_VOLLEY = 3       # shoot once this many are stored
HOOD_ANGLE = 0             # launch angle for shooting
RUN_LIMIT_S = None         # e.g. 120 to stop automatically after 2 minutes

# ------------------------------------------------------------------- STATES --
SEARCH, APPROACH, BLIND, SHOOT = "SEARCH", "APPROACH", "BLIND", "SHOOT"


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


class _Print:
    """Stand-in hardware for --dry: prints every call."""

    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr):
        return lambda *a, **k: print(f"   [dry] {self.name}.{attr}{a}{k or ''}")


class FakeRobot:
    def __init__(self):
        self.drive = _Print("drive")
        self.intake = _Print("intake")

    def shoot(self, **kwargs):
        print(f"   [dry] shoot({kwargs})")
        time.sleep(1)

    def stop(self):
        print("   [dry] stop()")


class AutoBot:
    def __init__(self, robot, cap):
        self.robot = robot
        self.cap = cap
        self.state = SEARCH
        self.hits = 0
        self.last = None        # last detection (x_offset, size, y_frac)
        self.last_seen = 0.0
        self.stored = 0         # ASSUMED count; there's no hopper sensor

    def go(self, new_state):
        print(f"{self.state} -> {new_state}")
        self.state = new_state
        self.hits = 0

    # --- one step per camera frame ---------------------------------------
    def step(self, det):
        now = time.time()
        r = self.robot

        if self.state == SEARCH:
            self.hits = self.hits + 1 if det else 0
            if self.hits >= DETECT_FRAMES:
                r.drive.stop()
                r.intake.intake()          # conveyor on before we arrive
                self.last, self.last_seen = det, now
                self.go(APPROACH)
            else:
                r.drive.move(0, SEARCH_TURN)

        elif self.state == APPROACH:
            if det:
                self.last, self.last_seen = det, now
                x, size, y = det
                tol = ALIGN_TOL_NEAR if y > NEAR_Y else ALIGN_TOL
                turn = 0.0
                if abs(x) > 0.02:
                    mag = clamp(abs(TURN_GAIN * x), MIN_TURN, MAX_TURN)
                    turn = mag if x > 0 else -mag
                if abs(x) > tol:
                    r.drive.move(0, turn)                  # pivot to line up
                else:
                    r.drive.move(APPROACH_POWER, turn * 0.5)
            elif (self.last and self.last[2] >= HANDOFF_Y
                  and self.last[1] >= HANDOFF_SIZE):
                self.go(BLIND)                             # ball left the bottom
            elif now - self.last_seen > LOST_TIMEOUT:
                r.drive.stop()
                r.intake.stop()
                self.last = None
                self.go(SEARCH)                            # genuinely lost it

        elif self.state == BLIND:
            r.intake.intake()
            r.drive.move(APPROACH_POWER)                   # straight, no steering
            time.sleep(BLIND_INCHES / INCHES_PER_SEC)
            r.drive.stop()
            time.sleep(BLIND_SETTLE_S)
            r.intake.stop()
            self.stored += 1
            self.last = None
            for _ in range(3):                             # drop stale frames
                self.cap.grab()
            print(f"   balls stored (assumed): {self.stored}")
            self.go(SHOOT if self.stored >= BALLS_PER_VOLLEY else SEARCH)

        elif self.state == SHOOT:
            r.drive.stop()
            r.shoot(balls=self.stored, hood_angle=HOOD_ANGLE)
            self.stored = 0
            self.go(SEARCH)


# --------------------------------------------------------------------- MAIN --
def open_camera(index):
    backend = cv2.CAP_DSHOW if sys.platform == "win32" else cv2.CAP_ANY
    cap = cv2.VideoCapture(index, backend)
    if not cap.isOpened():
        print(f"Could not open camera {index}")
        sys.exit(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)    # must match the tuning size
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    return cap


def main():
    dry = "--dry" in sys.argv
    index = CAMERA
    if "--camera" in sys.argv:
        index = int(sys.argv[sys.argv.index("--camera") + 1])

    if dry:
        robot = FakeRobot()
    else:
        from robot import Robot
        robot = Robot()

    cap = open_camera(index)
    bot = AutoBot(robot, cap)
    start = time.time()
    print("Running. Ctrl+C to stop.")
    try:
        while True:
            if RUN_LIMIT_S and time.time() - start > RUN_LIMIT_S:
                print("run limit reached")
                break
            ok, frame = cap.read()
            if not ok:
                print("Camera stopped giving frames")
                break
            bot.step(find_ball(frame))
    except KeyboardInterrupt:
        pass
    finally:
        robot.stop()
        cap.release()
        print("stopped")


if __name__ == "__main__":
    main()