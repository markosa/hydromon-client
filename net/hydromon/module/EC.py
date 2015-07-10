'''
Created on May 6, 2015

@author: markos
'''

import net.hydromon.dto.sensordto  # @UnusedImport
import logging
import smbus
import time
import os
from ec.miniec import MiniEC
import numpy

log = logging.getLogger(__name__)
DEVICE_BASE_DIR_1WIRE_BUS ='/sys/bus/w1/devices'



class EC():
 
    serial = None
    device = None 
    sensorId = None
    i2c_address = None
    i2c_smbusid = None
    i2c_configuration = None
    temperature_probe = None
    temperature_compensation_alpha = None
    
    ec_calibration_temperature = 22.00;
    
    use_average = 1

    miniec = None
    
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
            if option.startswith("temperature_probe"):
                self.temperature_probe = str(option.split(":")[1])     
            if option.startswith("temperature_compensation_alpha"):
                self.temperature_compensation_alpha = float(option.split(":")[1])         
       
        if not os.path.exists(self.i2c_configuration):
            raise IOError("Configuration file %s does not exist" % self.i2c_configuration)
        
        log.info("Initializing i2c ec interface at %s" + str(self.i2c_address) )
        self.miniec = MiniEC(self.i2c_address, self.i2c_smbusid)
        self.miniec.readConfig(self.i2c_configuration)
                      
        log.info("init passed")
        
    def testConfig(self):
    
        pass

    def readDevice(self, device): 
        lines = None
        try:
            f = open(device, 'r')
            lines = f.readlines()
            f.close()
        except:
            log.fatal("Unable to read device: " + device)
        return lines
        
    def readTemperature(self):
        device=DEVICE_BASE_DIR_1WIRE_BUS + '/' + self.temperature_probe + '/w1_slave'
        temp_c = None
        lines = self.readDevice(device)
        if lines is not None:
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self.readDevice()
                 
            equals_pos = lines[1].find('t=')
            
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:] 
                temp_c = float(temp_string) / 1000.0 
                log.debug(self.serial+": "+ str(temp_c) +" C")
                
        return float(temp_c)

    def read(self):
        ':type miniec: ec.miniec.MiniEC'
        
        
        ecvalues = []
        ec = 0
        for count in range(1,self.use_average + 1):
            tmpec = self.miniec.readEC()
            ecvalues.append(tmpec)
            #log.debug("EC: %s" % str(tmpec))
            ec = ec + tmpec
            time.sleep(0.5)
        
        ec = ec / count
        
        roundedec = round((median(ecvalues)/1000),2)
        log.debug("AVERAGE EC: " + str(ec))
        log.debug("ROUNDED EC: " + str(roundedec))
        log.debug("MEDIAN EC: " + str(median(ecvalues)))
 
        medianEC = (median(ecvalues)/1000)
 
        solutionTemperature = self.readTemperature()

        compensatedEC = self.calcTemperatureCompensation(medianEC, solutionTemperature)
        log.debug("TEMPERATURE: " + str(solutionTemperature) )
        log.debug("MEDIAN EC: " + str(medianEC))
        log.debug("COMPENSATED EC: " + str(compensatedEC))
 
        return round(compensatedEC, 2)

    def calcTemperatureCompensation(self, ec, temperature):
        Tcal = self.ec_calibration_temperature
        ecTcal = 1.1413;
        T = temperature
        log.debug("EC: " + str(ec))
        log.debug("Tcal: " + str(Tcal))
        log.debug("T: " + str(T))
        log.debug("alpha: " + str(self.temperature_compensation_alpha))

        ''' https://en.wikipedia.org/wiki/Electrical_conductivity_meter#Temperature_dependence '''
        
        ecT = ecTcal * (1 + self.temperature_compensation_alpha * (T - Tcal))
        
        return ecT

    
def median(lst):
    return numpy.median(numpy.array(lst))
