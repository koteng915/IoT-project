# IoT-project
IoT project for Software Engineering course (SKEL413) on Flood Monitoring System

## Problem Statement
Flood is a major known natural disaster that causes a huge amount of loss to the environment and living beings. So in these conditions, it is most crucial to get the emergency alerts of water level status at river beds in different conditions. In this project, the objective is to sense the water levels at river beds and check whether they are at a normal condition or not.

## System Architecture
![system architecture](https://user-images.githubusercontent.com/94040083/147046684-43c0744f-665b-4bf8-b4fe-7f2ab068594a.jpg)

## Sensor
The sensor we use is HC-SR04 Ultrasonic Sensor. The ultrasonic sensor works on the principle of ultrasound waves which is used to determine the distance to an object. 

![image](https://user-images.githubusercontent.com/94040083/147049018-50cd8e7e-518d-4c57-b478-600a1af922a5.png)

<details>
<summary>Flood monitoring code</summary>
<code style="white-space:nowrap;">
  
from machine import Pin, time_pulse_us
from utime import sleep_us

__version__ = '0.2.1'
__author__ = 'Roberto Sánchez'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.

    The timeouts received listening to echo pin are converted to OSError('Out of range')

    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        """
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin. 
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)

        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            # time_pulse_us returns -2 if there was timeout waiting for condition; and -1 if there was timeout during the main measurement. It DOES NOT raise an exception
            # ...as of MicroPython 1.17: http://docs.micropython.org/en/v1.17/library/machine.html#machine.time_pulse_us
            if pulse_time < 0:
                MAX_RANGE_IN_CM = const(500) # it's really ~400 but I've read people say they see it working up to ~460
                pulse_time = int(MAX_RANGE_IN_CM * 29.1) # 1cm each 29.1us
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms


</code>
</details>



## Cloud Platform
ThingSpeak is a software which can communicate with internet enabled devices. ThingSpeak can store the data in the channel and analyze it.

## Dashboard
link: https://thingspeak.com/channels/1615673
![image](https://user-images.githubusercontent.com/94040083/153732952-b4d6241d-92e0-4bbc-8236-fc0e859ccc0f.png)
