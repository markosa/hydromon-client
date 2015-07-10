'''
Created on May 6, 2015

@author: markos
'''

import logging
from time import sleep

import net.hydromon.dto.sensordto  # @UnusedImport
import time


log = logging.getLogger(__name__)

try:
    import RPIO
except:
    log.fatal("Cannot import RPIO library")

class YFS201():
    '''
    classdocs
    '''
    serial = None
    device = None 
    sensorId = None
    gpio_pin = None
    flow_ticks = 0


    def gpio_callback(self,gpio_id, val):
        self.flow_ticks = self.flow_ticks + 1
 
   
    def __init__(self, sensor):
        ':type sensor: net.hydromon.dto.sensordto.Sensor'
        self.serial=sensor.serial
        self.sensorId=sensor.sensorId
        self.gpio_pin=sensor.gpio_pin
        self.flow_ticks=0
        self.initializeInterrupt()
    
        
    def initializeInterrupt(self):
        log.info("Initializing interrupt for pin (RPIO.BCM) #" + str(self.gpio_pin)) 
        try:
            RPIO.setmode(RPIO.BCM)
            RPIO.setup(int(self.gpio_pin),RPIO.IN, pull_up_down=RPIO.PUD_UP)
            RPIO.add_interrupt_callback(int(self.gpio_pin), self.gpio_callback, edge='rising') 
            RPIO.wait_for_interrupts(threaded=True)
        except:
            log.error("RPIO library is missing")
        
        
    def testConfig(self):
        pass
        
    def read(self):
        self.flow_ticks=0
       
        # Use while loop instead of sleep(), sleep blocks thread
        currentTime=time.time()
        while currentTime+10 > time.time():
            pass
        
        flow_frequency = self.flow_ticks / 10.00
   
        
        
        
        litres_per_min = (flow_frequency / 7.5); # (Pulse frequency x 60 min) / 7.5Q = flow rate in L/hour 
        log.debug("Sensor is running at " + str(litres_per_min) +"L/min - total ticks in second " + str(flow_frequency))
        
        
        return round(litres_per_min,1)
        

    