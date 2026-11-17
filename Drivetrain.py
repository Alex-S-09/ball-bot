from motors import MotorDriver


class Drivetrain:
    """forward and turn are -1..1; turn > 0 = clockwise."""

    def __init__(self, left=(12, 5), right=(13, 6)):
        # each tuple is (pwm_pin, dir_pin); right is mirrored, so it's reversed
        self.left = MotorDriver(*left)
        self.right = MotorDriver(*right, reversed_=True)

    def move(self, forward, turn=0):
        self.left.set_power(forward + turn)
        self.right.set_power(forward - turn)

    def stop(self):
        self.left.stop()
        self.right.stop()