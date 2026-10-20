import time
from pitop import EncoderMotor, ForwardDirection

class Flywheel:
    
    def __init__(self, port="M2", power=1.0, spin_up_s=1.5):
        self.motor = EncoderMotor(port, ForwardDirection.CLOCKWISE)
        self.power = power
        self.spin_up_s = spin_up_s

    def spin_up(self):
        self.motor.set_power(self.power)
        time.sleep(self.spin_up_s)

    def off(self):
        self.motor.stop()