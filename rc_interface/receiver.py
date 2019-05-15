import logging
from time import sleep
import platform
# Import depends on which board is being used
try:
    import Adafruit_PCA9685
except ImportError:
    pass
try:
    import mraa_pca9685
except ImportError:
    pass

"""
This will allow you to interface to the normal inputs to an RC car.
There is the speed controller (ESC) and the steering servo
"""
FREQ = 60
board = platform.machine()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PCA9865:
    def __init__(self, channel, min, mid, max):
        # ESC stands for Electronic Speed Control
        self.channel = channel
        if board == 'aarch64':
            print('Setting up for Dragonboard')
            self.pwm = mraa_pca9685.PCA9685()
        else:
            self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(FREQ)
        self.min_value = -1
        self.max_value = 1
        self.max_pwm = max
        self.min_pwm = min

    def __enter__(self):
        return self

    def __del__(self):
        self.stop()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def stop(self):
        self.set(0)

    def set(self, value):
        pwm_value = self.map_value(value)
        self.pwm.set_pwm(self.channel, 0, pwm_value)

    def map_value(self, value):
        input_range = self.max_value - self.min_value
        output_range = self.max_pwm - self.min_pwm
        input_percentage = (value - self.min_value) / input_range
        output_value = (output_range * input_percentage) + self.min_pwm
        logger.debug('Input: {} - Output: {}', value, output_value)
        return int(output_value)


class SpeedController:
    """

    """
    def __init__(self):
        # ESC stands for Electronic Speed Control
        self.pwm_channel = 0
        self.min_pwm = 320
        self.mid_pwm = 420
        self.max_pwm = 520
        self.esc = PCA9865(self.pwm_channel,
                           self.min_pwm,
                           self.mid_pwm,
                           self.max_pwm)

    def stop(self):
        self.esc.set(0)

    def speed(self, position):
        self.esc.set(position)


class Steering:
    def __init__(self):
        # ESC stands for Electronic Speed Control
        self.pwm_channel = 1
        self.min_pwm = 320
        self.mid_pwm = 420
        self.max_pwm = 520
        self.rack = PCA9865(self.pwm_channel,
                            self.min_pwm,
                            self.mid_pwm,
                            self.max_pwm)

    def neutral(self):
        self.rack.set(0)

    def position(self, value):
        self.rack.set(value)


if __name__ == '__main__':
    steering = Steering()
    for x in range(-10, 11):
        steering.position(x/10)
        print(x/10)
        sleep(0.5)
    steering.neutral()

    speed = SpeedController()
    for y in range(0, 11):
        print(y/10)
        speed.speed(y/10)
        sleep(0.5)
    speed.stop()
