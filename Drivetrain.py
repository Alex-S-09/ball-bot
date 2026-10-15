from pitop import EncoderMotor, ForwardDirection

class Drivetrain:

    def __init__(self, left_port="M0", right_port="M3"):
        self.left = EncoderMotor(left_port, ForwardDirection.CLOCKWISE)
        self.right = EncoderMotor(right_port, ForwardDirection.COUNTER_CLOCKWISE)

    def move(self, forward, turn=0):
        self.left.set_power(max(-1, min(1, forward + turn)))
        self.right.set_power(max(-1, min(1, forward - turn)))

    def stop(self):
        self.left.stop()
        self.right.stop()