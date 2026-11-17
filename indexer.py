import time
from gpiozero import Servo


class Indexer:
    """Continuous-rotation servo that feeds exactly one ball per release."""

    def __init__(self, pin=27, speed=0.5, spin_s=0.4, settle_s=0.4):
        self.servo = Servo(pin)
        self.speed = speed        # -1..1; sign sets direction
        self.spin_s = spin_s      # spin time per ball: TUNE THIS
        self.settle_s = settle_s
        self.close()

    def close(self):
        """Stop the servo by cutting its signal entirely (no creeping)."""
        self.servo.detach()

    def release_one(self):
        self.servo.value = self.speed
        time.sleep(self.spin_s)
        self.close()
        time.sleep(self.settle_s)