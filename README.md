# runfan
Short fan controller for Raspberry Pi

This is a SUPER SIMPLE controller to start and stop a fan based on temperature thresholds, via a GPIO pin. 

DO NOT PLUG THE FAN DIRECTLY INTO THE GPIO PIN!!!! Fans draw a lot more current than can be provided by a 
GPIO pin.

Instead, use a relay or transistor to control the fan. The GPIO turns on the relay or transistor and that in
turn turns on the fan.

If you are using a transistor, make certain that the transistor is rated to pass enough current for the fan.


Save runfan.py on your pi somewhere such as /home/pi/bin/runfan.

Make it executable:
```
chmod a+x /home/pi/fan/runfan
```

Then execute it using 

```
runfan delay ontemp offtemp gpiopin
```

where you fill in appropriate values. For example, to check the temperature every 15 seconds, 
turn the fan on at 65°C, turn it back off at 55°C, and use GPIO 23 (physical pin 12) to control it, 
you would run it using:

```
runfan 15 65 55 23
```

This will display a message each time `runfan` checks the temperature telling you what the current state is.

If you want this to run at boot, add a line to the end of `/etc/rc.local` (before any exit lines) that looks 
like one of these lines:

```
# Run the fan, saving the messages to /tmp/runfan.log
runfan 15 65 55 23 > /tmp/runfan.log &
# Run the fan, turning off the messages
runfan 15 65 55 23 > /dev/null &
```
