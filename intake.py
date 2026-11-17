from motors import MotorDriver


class Intake:
    def __init__(self, pins=(18, 23), power=0.8):
        self.motor = MotorDriver(*pins)
        self.power = power

    def intake(self):
        self.motor.set_power(self.power)

    def reverse(self):
        self.motor.set_power(-self.power)

    def stop(self):
        self.motor.stop()