'''
Created on May 6, 2015

@author: markos
'''

import net.hydromon.dto.sensordto  # @UnusedImport
import logging
import time

log = logging.getLogger(__name__)

DEVICE_BASE_DIR='/sys/bus/w1/devices'

class DS18B20():
    '''
    classdocs
   
    Read logic copied from this article
    https://learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf
    
    '''
    serial = None
    device = None 
    sensorId = None
   
    def __init__(self, sensor):
        ':type sensor: net.hydromon.dto.sensordto.Sensor'
        self.serial=sensor.serial
        self.device=DEVICE_BASE_DIR + '/' + self.serial + '/w1_slave'
        self.sensorId=sensor.sensorId
        
    def testConfig(self):
        #self.read()
        pass
     
    def readDevice(self): 
        f = open(self.device, 'r')
        lines = f.readlines()
        f.close()
        return lines
        
    def read(self):
        '''
        lines = self.readDevice()
        
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.readDevice()
             
        equals_pos = lines[1].find('t=')
        
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:] 
            temp_c = float(temp_string) / 1000.0 
        '''
        temp_c = 20
        return temp_c
        

    