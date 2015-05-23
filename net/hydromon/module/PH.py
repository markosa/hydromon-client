'''
Created on May 6, 2015

@author: markos
'''

import net.hydromon.dto.sensordto  # @UnusedImport
import logging
import smbus
import time
import os
from ph.miniph import MiniPH

log = logging.getLogger(__name__)


class PH():
 
    serial = None
    device = None 
    sensorId = None
    i2c_address = None
    i2c_smbusid = None
    i2c_configuration = None
    use_average = 1

    miniph = None
    
    def __init__(self, sensor):
        ':type sensor: net.hydromon.dto.sensordto.Sensor'
        self.serial = sensor.serial
        self.sensorId = sensor.sensorId
        self.gpio_pin = sensor.gpio_pin
        
        options = sensor.moduleOptions.split(';')
        for option in options: 
            if option.startswith("i2c_address"):
                self.i2c_address = str(option.split(":")[1])
            if option.startswith("i2c_smbusid"):
                self.i2c_smbusid = int(option.split(":")[1])  
            if option.startswith("i2c_configuration"):
                self.i2c_configuration = str(option.split(":")[1])
            if option.startswith("use_average"):
                self.use_average = int(option.split(":")[1])
        
        if not os.path.exists(self.i2c_configuration):
            raise IOError("Configuration file %s does not exist" % self.i2c_configuration)

        
        
        log.info("Initializing i2c ph interface at %s" + str(self.i2c_address) )
        self.miniph = MiniPH(self.i2c_address, self.i2c_smbusid)
        self.miniph.readConfig(self.i2c_configuration)
                      
        log.info("init passed")
        
    def testConfig(self):
        pass
     
        
    def read(self):
        ':type miniph: ph.miniph.MiniPH'
        
        
        ph = 0
        for count in range(1,self.use_average + 1):
            tmpph = self.miniph.readPH()
            log.debug("PH: %s" % str(tmpph))
            ph = ph + tmpph
            time.sleep(2)
        
        ph = ph / count
        
        log.debug("AVERAGE PH: " + str(ph))
        
        roundedph = round(ph,2)

        log.debug("ROUNDED PH: " + str(roundedph))

        return roundedph

    
