#!/usr/bin/env python3

"""
Manage a fan based on threshold temperatures.
"""

# See LICENSE file for sharing purposes
# Copyright 2019-2020 Tony Hansen

import argparse
import sys
import time
import psutil
import gpiozero

DEF_ON = 65.0
DEF_OFF = 55.0
DEF_DELAY = 5.0
DEF_GPIO = 23

def main():
    """ main program execution """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--off-threshold', "-o", type=float, default=DEF_OFF,
                        help=f'Temperature threshold in degrees C to enable fan, default={DEF_OFF}')
    parser.add_argument('--on-threshold', "-O", type=float, default=DEF_ON,
                        help=f'Temperature threshold in degrees C to disable fan, default={DEF_ON}')
    parser.add_argument('--delay', "-d", type=float, default=DEF_DELAY,
                        help=f'Delay, in seconds, between temperature readings, default={DEF_DELAY}')
    parser.add_argument('--gpio', "-g", type=int, default=DEF_GPIO, help=f'GPIO BCM number, default={DEF_GPIO}')
    parser.add_argument('--verbose', "-v", action='store_true', default=False,
                        help='Output temp and fan status messages')

    args = parser.parse_args()

    if args.on_threshold < args.off_threshold:
        sys.exit(f"--on-threshold {args.on_threshold} must be greater than --off-threshold {args.off_threshold}")

    try:
        fan_on = False
        fan = gpiozero.OutputDevice(args.gpio)
        while True:
            # get CPU temperature. Some systems spell it 'cpu-thermal' and others 'cpu_thermal'
            ptemp = psutil.sensors_temperatures()
            cur_temp = ptemp['cpu-thermal'][0].current if 'cpu-thermal' in ptemp \
                else ptemp['cpu_thermal'][0].current if 'cpu_thermal' in ptemp \
                     else -9999
            if cur_temp == -9999:
                print("Cannot determine the CPU temperature", file=sys.stderr)
            old_fan_on = fan_on
            # if past either boundary, turn it on or off
            if not fan_on and cur_temp >= args.on_threshold:
                fan.on()
                fan_on = True
            elif fan_on and cur_temp <= args.off_threshold:
                fan.off()
                fan_on = False
            if args.verbose:
                print(f"{time.ctime()}: {cur_temp} {old_fan_on} => {fan_on}")
            time.sleep(args.delay)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
