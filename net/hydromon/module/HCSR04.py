'''
Created on May 6, 2015

@author: markos
'''

import net.hydromon.dto.sensordto  # @UnusedImport
import logging
import time
import RPi.GPIO as GPIO
from net.hydromon.module import SensorTimedOutError

log = logging.getLogger(__name__)

DEVICE_BASE_DIR = '/sys/bus/w1/devices'

class HCSR04():
    '''
    classdocs
   
    http://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
    
    http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/
    
    '''
    serial = None
    device = None 
    sensorId = None
    gpio_pin = None
    trigger_gpio_pin = None
    echo_gpio_pin = None
    

    def __init__(self, sensor):
        ':type sensor: net.hydromon.dto.sensordto.Sensor'
        self.serial = sensor.serial
        self.sensorId = sensor.sensorId
        self.gpio_pin = sensor.gpio_pin
        
        options = sensor.moduleOptions.split(';')
        for option in options: 
            if option.startswith("gpio_pin_trig"):
                self.trigger_gpio_pin = int(option.split(":")[1])
            if option.startswith("gpio_pin_echo"):
                self.echo_gpio_pin = int(option.split(":")[1])        
        log.info("init passed")
        
    def testConfig(self):
        # self.read()
        pass
     
        
    def read(self):
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.trigger_gpio_pin, GPIO.OUT)  # Trigger
        GPIO.setup(self.echo_gpio_pin, GPIO.IN)   
        
        GPIO.output(self.trigger_gpio_pin, False)
        
        time.sleep(0.5)

        GPIO.output(self.trigger_gpio_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_gpio_pin, False)

        start = time.time()
        controlTime = time.time()
        try:
            while GPIO.input(self.echo_gpio_pin) == 0:
                start = time.time()
             #   if (controlTime + 5 < time.time()):
             #       raise SensorTimedOutError('Cannot get LOW reading from Echo pin %s' + str(self.echo_gpio_pin))
                    
            controlTime = time.time()
            while GPIO.input(self.echo_gpio_pin) == 1:
                stop = time.time()
             #   if (controlTime + 30 < time.time()):
             #       raise SensorTimedOutError('Now response from the sensor in 30 secs, giving up')     
            elapsed = stop - start
            distance = elapsed * 34300
            distance = distance / 2
            distance = round(distance, 2)
            log.debug("Distance : %.1f" % distance)
            
            return distance
        except SensorTimedOutError as stoe:
                log.warn(stoe)
    
        return '-1'

    
