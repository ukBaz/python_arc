from time import sleep

from pydbus import SystemBus
import evdev

# For testing
# python3 -m evdev.evtest
red = ['40:1B:5F:8E:BF:2A', '/org/bluez/hci0/dev_40_1B_5F_8E_BF_2A']
blue = ['DC:0C:2D:20:DA:E8', '/org/bluez/hci0/dev_DC_0C_2D_20_DA_E8']
my_dev = blue


class Controller:

    def __init__(self, adapter_int=0):
        adapter_path = '/org/bluez/hci{}'.format(adapter_int)
        self.dbus = SystemBus()
        self.adapter = self.dbus.get('org.bluez', adapter_path)
        self.controller = self.dbus.get('org.bluez',
                                        my_dev[1])
        print('Waiting for connection from', my_dev[0])
        self.controller.Connect()
        while not self.controller.Connected:
            sleep(1)
        print('Connected')
        sleep(2)
        self.device = evdev.InputDevice('/dev/input/event1')
        self.max_value = 0
        self.min_value = 255
        self.max_throttle = 1
        self.min_throttle = -1
        self.right_steering = 1
        self.left_steering = -1

    def map_throttle(self, value):
        input_range = self.max_value - self.min_value
        output_range = self.max_throttle - self.min_throttle
        input_percentage = (value - self.min_value) / input_range
        output_value = (output_range * input_percentage) + self.min_throttle
        return round(output_value, 2)

    def map_steering(self, value):
        input_range = self.max_value - self.min_value
        output_range = self.right_steering - self.left_steering
        input_percentage = (value - self.min_value) / input_range
        output_value = (output_range * input_percentage) + self.left_steering
        return round(output_value, 2)

    def get_events(self):
        for event in self.device.read_loop():
            ly = None
            rx = None
            btn = None
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == 1:
                    # print('Left:', event.value)
                    ly = self.map_throttle(event.value)
                if event.code == 3:
                    # print('Right:', event.value)
                    rx = self.map_steering(event.value)
            if event.type == evdev.ecodes.EV_KEY:
                if event.code == evdev.ecodes.BTN_SOUTH and event.value == 0:
                    btn = 'BTN_SOUTH'
                elif event.code == evdev.ecodes.BTN_WEST and event.value == 0:
                    btn = 'BTN_WEST'
                elif event.code == evdev.ecodes.BTN_NORTH and event.value == 0:
                    btn = 'BTN_NORTH'
                elif event.code == evdev.ecodes.BTN_EAST and event.value == 0:
                    btn = 'BTN_EAST'
            yield ly, rx, btn


if __name__ == '__main__':
    ctrl = Controller()
    for speed, steer, action in ctrl.get_events():
        print(speed, steer, action)
