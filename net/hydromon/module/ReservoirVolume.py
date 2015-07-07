'''
Created on May 6, 2015

@author: markos
'''

import net.hydromon.dto.sensordto  # @UnusedImport
import logging
import HCSR04 as hc
import numpy

from net.hydromon.module import SensorTimedOutError

log = logging.getLogger(__name__)

DEVICE_BASE_DIR = '/sys/bus/w1/devices'

class ReservoirVolume():
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
    sensor_distance = None
    reservoir_length = None
    reservoir_width = None
    reservoir_height = None
    reservoir_multiplier = 1
    
    
    
    def calculateVolume(self, l,w,h):
        return l*w*h
    
    def cubicCentiMetersToLitres(self, cm3):
        return cm3 / 1000.00
  
    def calculateCurrentVolume(self):
        
        values = []
        
        for count in range(1,10):
            uSeconds = hc.readvalue(self.trigger_gpio_pin, self.echo_gpio_pin)
            values.append(uSeconds)
        
        uSeconds = median(values)
    
        distance = uSeconds * ( 343.59 / 1000000.0000 ) # time in us * ( speed of sound m/s / 10e6 ) -> m/us -> m
        distance = distance * 100 # m -> cm
        distance = distance / 2 # signal from sensor is traveling to surface and back thus dividing by two
        log.debug("Distance: " + str(distance))
        
        liquidHeight = self.sensor_distance - distance
        
        volume = self.calculateVolume(self.reservoir_length, self.reservoir_width, liquidHeight)

        litres = self.cubicCentiMetersToLitres(volume) * self.reservoir_multiplier # litres multiplied by multiplier, in my setup I have two plastic boxes connected to each other, water will level between boxes by physics

        log.debug("Litres: " + str(litres))

        return round(litres) 
    
    
    
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
            if option.startswith("sensor_distance"):
                self.sensor_distance = int(option.split(":")[1])        
            if option.startswith("reservoir_length"):
                self.reservoir_length = int(option.split(":")[1])        
            if option.startswith("reservoir_width"):
                self.reservoir_width = int(option.split(":")[1])        
            if option.startswith("reservoir_height"):
                self.reservoir_height = int(option.split(":")[1])        
            if option.startswith("reservoir_multiplier"):
                self.reservoir_multiplier = int(option.split(":")[1])        
        
        ''' reservoir_length=76;reservoir_width=47;reservoir_height=51;sensor_distance=84 '''
        capacity =  self.cubicCentiMetersToLitres(self.calculateVolume(self.reservoir_length, self.reservoir_width, self.reservoir_height)) * self.reservoir_multiplier
        log.info("Sensor initialized. Maximum capacity is " + str(capacity) + " litres ")
        
    def testConfig(self):
        pass
     
        
    def read(self):
        return self.calculateCurrentVolume()
    
 
     
def median(lst):
    return numpy.median(numpy.array(lst))   
