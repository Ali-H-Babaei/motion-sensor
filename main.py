import argparse
from MotionSensor import MotionSensor


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bridge", help="Bridge, or hub, IP address")
    parser.add_argument("-u", "--username", help="Username created for interacting with the Hue Bridge")
    parser.add_argument("-i", "--interval", help="Interval in seconds to check motion sensor")
    parser.add_argument("-s", "--sensor", help="Sensor to monitor")
    args = parser.parse_args()

    if args.bridge and args.username:
        motion_sensor = MotionSensor(args.bridge, args.username, args.interval, args.sensor)
        motion_sensor.run()

