from pitop import EncoderMotor, ForwardDirection

try:
    from pitop.pma.parameters import Direction
    HAS_DIRECTION = True
except ImportError:
    HAS_DIRECTION = False


def make_motor(port, clockwise=True):
    direction = ForwardDirection.CLOCKWISE if clockwise else ForwardDirection.COUNTER_CLOCKWISE
    return EncoderMotor(port, direction)


def set_signed(motor, power):
    """Set power from -1 to 1, using the SDK's direction argument if it has one."""
    power = max(-1.0, min(1.0, power))
    if HAS_DIRECTION:
        direction = Direction.FORWARD if power >= 0 else Direction.BACKWARD
        motor.set_power(abs(power), direction)
    else:
        motor.set_power(power)