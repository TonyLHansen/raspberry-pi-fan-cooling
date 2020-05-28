#!/usr/bin/env python3

"""
Manage a fan on based on threshold temperatures.
"""

# See LICENSE file for sharing purposes
# Copyright 2019 Tony Hansen

import gpiozero, time, psutil, sys, argparse

def main():
    """ main program execution """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--off-threshold', "-o", type=float, default=55.0, help='Temperature threshold in degrees C to enable fan')
    parser.add_argument('--on-threshold', "-O", type=float, default=65.0, help='Temperature threshold in degrees C to disable fan')
    parser.add_argument('--delay', "-d", type=float, default=5.0, help='Delay, in seconds, between temperature readings')
    parser.add_argument('--gpio', "-g", type=int, default=23, help='GPIO BCM number')
    parser.add_argument('--verbose', "-v", action='store_true', default=False, help='Output temp and fan status messages')

    args = parser.parse_args()

    if args.on_threshold < args.off_threshold:
        sys.exit("--on-threshold ({}) must be greater than --off-threshold ({})".format(args.on_threshold, args.off_threshold))

    try:
        on = False
        fan = gpiozero.OutputDevice(args.gpio)
        while True:
            # get CPU temperature. Some systems spell it 'cpu-thermal' and others 'cpu_thermal'
            pt = psutil.sensors_temperatures()
            t = pt['cpu-thermal'][0].current if 'cpu-thermal' in pt \
                else pt['cpu_thermal'][0].current if 'cpu_thermal' in pt \
                     else -9999
            if t == -9999:
                print("Cannot determine the CPU temperature", file=sys.stderr)
            print("{}: {} {}".format(time.ctime(), t, on))
            # if past either boundary, turn it on or off
            if not on and t >= args.on_threshold:
                fan.on()
                on = True
            elif on and t <= args.off_threshold:
                fan.off()
                on = False
            time.sleep(args.delay)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
