import time
from motors import MotorDriver


class Flywheel:
    def __init__(self, pins=(19, 24), power=1.0, spin_up_s=1.5):
        self.motor = MotorDriver(*pins)
        self.power = power
        self.spin_up_s = spin_up_s

    def spin_up(self):
        self.motor.set_power(self.power)
        time.sleep(self.spin_up_s)

    def off(self):
        self.motor.stop()