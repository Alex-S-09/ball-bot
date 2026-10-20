from motors import make_motor, set_signed


class Intake:
    def __init__(self, port="M1", power=0.8):
        self.motor = make_motor(port, clockwise=True)
        self.power = power

    def intake(self):
        set_signed(self.motor, self.power)

    def reverse(self):
        set_signed(self.motor, -self.power)

    def stop(self):
        self.motor.stop()