from motors import make_motor, set_signed

class Drivetrain:
    """forward and turn are -1..1; turn > 0 = clockwise."""

    def __init__(self, left_port="M0", right_port="M3"):
        self.left = make_motor(left_port, clockwise=True)
        self.right = make_motor(right_port, clockwise=False)

    def move(self, forward, turn=0):
        set_signed(self.left, forward + turn)
        set_signed(self.right, forward - turn)

    def stop(self):
        self.left.stop()
        self.right.stop()