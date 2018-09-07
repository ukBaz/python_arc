import remote as rc
import receiver as car
import camera


def main():
    steering = car.Steering()
    throttle = car.SpeedController()
    eye = camera.Camera()
    car_enabled = False
    rec_enabled = False
    remote = rc.Controller()
    for speed, steer, action in remote.get_events():
        if speed and car_enabled:
            print('Speed', speed)
            throttle.speed(speed)
        if steer and car_enabled:
            print('Steer', steer)
            steering.position(steer)
        if action:
            if action == 'BTN_NORTH':
                print('Enable car')
                car_enabled = True
            elif action == 'BTN_EAST':
                print('Start recording')
                rec_enabled = True
                eye.open()
            elif action == 'BTN_SOUTH':
                print('Disable car')
                car_enabled = False
                throttle.stop()
                steering.neutral()
            elif action == 'BTN_WEST':
                print('Stop recording')
                rec_enabled = False
                eye.closed()


if __name__ == '__main__':
    main()

