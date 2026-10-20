import time
from pitop import ServoMotor


class Indexer:
    def __init__(self, port="S0", closed=-30, open_=30, open_s=0.25, settle_s=0.4):
        self.servo = ServoMotor(port)
        self.closed = closed
        self.open = open_
        self.open_s = open_s
        self.settle_s = settle_s  # wait after closing so a second release can't overlap
        self.close()

    def close(self):
        self.servo.target_angle = self.closed

    def release_one(self):
        self.servo.target_angle = self.open
        time.sleep(self.open_s)
        self.close()
        time.sleep(self.settle_s)