'''
Created on May 6, 2015

@author: markos
'''

import logging

import net.hydromon.dto.sensordto  # @UnusedImport


log = logging.getLogger(__name__)


class ModulePrototype():
    '''
    classdocs
   
    Read logic copied from this article
    https://learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf
    
    '''
   
    sensorId = None
    

   
    def __init__(self, sensor):
        ':type sensor: net.hydromon.dto.sensordto.Sensor'

    def testConfig(self):
        pass
                
    def read(self):
        pass

    