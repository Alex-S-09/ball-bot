from gpiozero import AngularServo


class Hood:
    """Adjustable hood that sets the launch angle."""

    def __init__(self, pin=17, min_angle=-40, max_angle=40):
        self.servo = AngularServo(pin, min_angle=-90, max_angle=90)
        self.min = min_angle      # your safe mechanical range
        self.max = max_angle
        self.angle = 0
        self.set_angle(0)

    def set_angle(self, angle):
        self.angle = max(self.min, min(self.max, angle))
        self.servo.angle = self.angle