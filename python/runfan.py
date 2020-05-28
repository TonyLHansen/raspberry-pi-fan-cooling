#!/usr/bin/env python3
# See LICENSE file for sharing purposes
# Copyright 2019 Tony Hansen

import gpiozero,time,psutil,sys

if len(sys.argv) != 5:
    sys.exit("Usage: {} delay ontemp offtemp gpiopin".format(sys.argv[0]))

delay = int(sys.argv[1])
ontemp = float(sys.argv[2])
offtemp = float(sys.argv[3])
gpiopin = int(sys.argv[4])

if ontemp < offtemp:
    sys.exit("ontemp ({}) must be greater than offtemp ({})".format(ontemp, offtemp))

on = False
fan = gpiozero.OutputDevice(gpiopin)

try:
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
        if not on and t >= ontemp:
            fan.on()
            on = True
        elif on and t <= offtemp:
            fan.off()
            on = False
        time.sleep(delay)
except KeyboardInterrupt:
    pass
