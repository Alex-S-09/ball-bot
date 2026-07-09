from pitop import BrakingType, EncoderMotor, ForwardDirection
import config

class Drivetrain

def __init__(self):
    self.front_left = EncoderMotor(config.FRONT_LEFT_MOTOR_PORT, ForwardDirection.CLOCKWISE)
    self.front_right = EncoderMotor(config.FRONT_RIGHT_MOTOR_PORT, ForwardDirection.COUNTER_CLOCKWISE)    
    self.back_left = EncoderMotor(config.BACK_LEFT_MOTOR_PORT, ForwardDirection.CLOCKWISE)
    self.back_right = EncoderMotor(config.BACK_RIGHT_MOTOR_PORT, ForwardDirection.COUNTER_CLOCKWISE)

    for motor in (self.front_left, self.front_right, self.back_left, self.back_right):
        motor.braking_type = BrakingType.COAST