from time import sleep
import mraa


class PCA9685:
    MODE1 = 0x00
    MODE2 = 0x01
    LED0_ON_L = 0x06
    LED0_ON_H = 0x07
    LED0_OFF_L = 0x08
    LED0_OFF_H = 0x09
    ALL_LED_ON_L = 0xFA
    ALL_LED_ON_H = 0xFB
    ALL_LED_OFF_L = 0xFC
    ALL_LED_OFF_H = 0xFD
    PRE_SCALE = 0xFE

    ALLCALL = 0x01
    OUTDRV = 0x04
    SLEEP = 0x10

    sleep_500us = 0.005

    def __init__(self, bus=1, i2c_addr=0x40):
        self.device = mraa.I2c(bus)
        self.device.address(i2c_addr)
        self._initialization()

    def _initialization(self):
        self.set_all_pwm(0, 0)
        self.device.writeReg(PCA9685.MODE2, PCA9685.OUTDRV)
        self.device.writeReg(PCA9685.MODE1, PCA9685.ALLCALL)
        sleep(PCA9685.sleep_500us)
        mode1_settings = self.device.readReg(PCA9685.MODE1)
        mode1_settings = mode1_settings & ~PCA9685.SLEEP
        self.device.writeReg(PCA9685.MODE1, mode1_settings)
        sleep(PCA9685.sleep_500us)

    def set_pwm_freq(self, freq):
        osc_clk = 25000000.0
        refresh_rate = int(osc_clk/(4096 * (freq + 1)))
        print('refresh rate', refresh_rate)
        current_mode = self.device.readReg(PCA9685.MODE1)
        sleep_mode = (current_mode & 0x7F) | 0x10
        self.device.writeReg(PCA9685.MODE1, sleep_mode)
        self.device.writeReg(PCA9685.PRE_SCALE, refresh_rate)
        self.device.writeReg(PCA9685.MODE1, current_mode)
        sleep(PCA9685.sleep_500us)
        self.device.writeReg(PCA9685.MODE1, current_mode | 0x80)

    def set_pwm(self, channel, on, off):
        self.device.writeReg(PCA9685.LED0_ON_L + 4 * channel, on & 0xFF)
        self.device.writeReg(PCA9685.LED0_ON_H + 4 * channel, on >> 8)
        self.device.writeReg(PCA9685.LED0_OFF_L + 4 * channel, off & 0xFF)
        self.device.writeReg(PCA9685.LED0_OFF_H + 4 * channel, off >> 8)

    def set_all_pwm(self, on, off):
        self.device.writeReg(PCA9685.ALL_LED_ON_L, on & 0xFF)
        self.device.writeReg(PCA9685.ALL_LED_ON_H, on >> 8)
        self.device.writeReg(PCA9685.ALL_LED_OFF_L, off & 0xFF)
        self.device.writeReg(PCA9685.ALL_LED_OFF_H, off >> 8)
