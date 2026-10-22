from gpiozero import PWMOutputDevice, DigitalOutputDevice


class MotorDriver:
    """One Cytron MD10C channel. power is -1..1 (sign = direction)."""

    def __init__(self, pwm_pin, dir_pin, reversed_=False, frequency=1000):
        self.pwm = PWMOutputDevice(pwm_pin, frequency=frequency)
        self.dir = DigitalOutputDevice(dir_pin)
        self.reversed = reversed_

    def set_power(self, power):
        power = max(-1.0, min(1.0, power))
        if self.reversed:
            power = -power
        if power >= 0:
            self.dir.on()
        else:
            self.dir.off()
        self.pwm.value = abs(power)

    def stop(self):
        self.pwm.value = 0