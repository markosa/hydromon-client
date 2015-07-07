'''
Created on May 22, 2015

@author: Marko Sahlman
'''

try:
    import smbus
except:
    print "error"
    
import ConfigParser
import logging
import argparse
import os
import sys
import time
log = logging.getLogger(__name__)

class MiniEC(object):
    '''
    classdocs
    
    
    http://www.sparkyswidgets.com/portfolio-item/miniph-i2c-ph-interface/
    
    '''
    eC = None
    I2CadcVRef = 4948 # In raspberry this should be 3300mV but may vary!
    oscV = 185 # '''voltage of oscillator output after voltage divider in millivolts i.e 120mV (measured AC RMS) ideal output is about 180-230mV range'''
    
    kCell = 1.00 # set our Kcell constant basically our microsiemesn conversion 10-6 for 1 10-7 for 10 and 10-5 for .1'''
    Rgain = 3000.0 # //this is the measured value of the R9 resistor in ohms

    ecLowCal = 0
    ecHighCal = 0
    ecLowCalValue= 0
    ecHighCalValue= 0
    
    ecCalTemp = 22.0 # This is calibration liquid's temperature, assume 22 degrees of celcius. 
    ecStep = None
    
    def __init__(self, address,smbusid=1, vref=3300.00, opampGain=5.25):
        '''
        Constructor
        '''
        self.i2c_smbusid=smbusid
        self.i2c_address=address
        self.I2CadcVRef=vref
        self.bus=smbus.SMBus(smbusid)
        self.opampGain=opampGain 
        
        
    def readRawValue(self):
        data = self.bus.read_i2c_block_data(int(self.i2c_address,16), 1,2)
        high = data[0]
        low = data[1]
        adc_result = (high * 256) + low
        return adc_result

    def calibrateLow(self):
        rawvalue=0
        for count in range(1,100):
            rawvalue = rawvalue + self.readRawValue()
            time.sleep(0.1)
        
        self.ecLowCal=rawvalue / count
        self.calculateSlope()
    
    def calibrateHigh(self):
        rawvalue=0
        for count in range(1,100):
            rawvalue = rawvalue + self.readRawValue()
            time.sleep(0.1)
       
        self.ecHighCal = rawvalue / count
       
        self.calculateSlope()
    
    def calculateSlope(self):
        ec_raw_delta = self.ecHighCal - self.ecLowCal
        ec_delta = self.ecHighCalValue - self.ecLowCalValue
        self.ecStep = ec_delta / ec_raw_delta
        return self.ecStep
        
    def calcEC(self,raw):
        # miliVolts = ((raw/4096.0)*self.vref)*1000 
        # temp = ((((self.vref*self.pH7Cal)/4096.0)*1000)- miliVolts)/self.opampGain
        # pH = 7-(temp/self.pHStep)
        raw = self.readRawValue()
        ec = (raw - self.ecLowCal) * self.ecStep
        #print "RAW: " + str(raw)
        #print "EC: " + str(ec)
        return round(ec)

    def readEC(self):
        return self.calcEC(self.readRawValue())

    def writeConfig(self,configfile):
        config = ConfigParser.RawConfigParser()
        configsection = "miniec_%s" % self.address 
        config.add_section(configsection)
        ''' smbusid=1, address=0x4e, vref=3.3, opampGain=5.25 '''
        config.set(configsection, 'smbusid', self.i2c_smbusid)
        config.set(configsection, 'address', self.i2c_address)
        config.set(configsection, 'opampGain', self.opampGain)
        config.set(configsection, 'ecLowCal', self.ecLowCal)
        config.set(configsection, 'ecHighCal', self.ecHighCal)
        config.set(configsection, 'ecLowCalValue', self.ecLowCalValue)
        config.set(configsection, 'ecHighCalValue', self.ecHighCalValue)
        config.set(configsection, 'ecCalTemp', self.ecCalTemp)
        config.set(configsection, 'ecStep', self.ecStep)
        config.set(configsection, 'vref', self.I2CadcVRef)

        with open(configfile, 'wb') as configfile:
            config.write(configfile)
        
    
    def readConfig(self,configfile):
        config = ConfigParser.RawConfigParser()

        configsection = "miniec_%s" % self.i2c_address 
        config.read(configfile)
        self.i2c_smbusid = config.get(configsection, 'smbusid')
        self.i2c_address = config.get(configsection, 'address')
        self.opampGain = float(config.get(configsection, 'opampGain'))
        self.ecLowCal = float(config.get(configsection, 'ecLowCal'))
        self.ecHighCal = float(config.get(configsection, 'ecHighCal'))
        self.ecLowCalValue = float(config.get(configsection, 'ecLowCalValue'))
        self.ecHighCalValue = float(config.get(configsection, 'ecHighCalValue'))
        
        self.ecCalTemp = float(config.get(configsection, 'ecCalTemp'))
        self.ecStep = float(config.get(configsection, 'ecStep'))
        self.I2CadcVRef = float(config.get(configsection,'vref'))
        
        self.calculateSlope()
        

if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(description='Read or calibrate ec probe. Calibrate using --eclow and --echigh flags.')
    parser.add_argument('busid', metavar='BUSID', type=int, nargs='?',help='I2C bus id. Ie. 0 or 1')    
    parser.add_argument('address', metavar='ADDRESS', type=str, nargs='?',help='I2C Address. Ie. 0x4d')    

    parser.add_argument('--configfile', help='config file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--eclow', action='store_true')
    group.add_argument('--echigh', action='store_true')
    
    
    
    args = parser.parse_args()  
    
    if  not args.address or not args.busid:
            parser.print_usage()
            sys.exit(1)
            
    if not args.eclow and not args.echigh:
        if args.configfile and os.path.exists(args.configfile):
            eci2c = MiniEC(args.address, args.busid)
            eci2c.readConfig(args.configfile)
            print str(eci2c.readEC())
        else:
            parser.print_usage()
            print "\nError: no config file given or it does not exist. Calibrate and save config or give new config file location"
            sys.exit(1)

    elif args.eclow:
            eci2c = MiniEC(args.address, args.busid)
            if os.path.exists(args.configfile):
                eci2c.readConfig(args.configfile)
            eci2c.calibrateLow()
            eci2c.writeConfig(args.configfile)
            print "Calibrated LOW point and wrote config %s" % args.configfile
    elif args.echigh:
            eci2c = MiniEC(args.address, args.busid)
            if os.path.exists(args.configfile):
                eci2c.readConfig(args.configfile)
            eci2c.calibrateHigh()
            eci2c.writeConfig(args.configfile)        
            print "Calibrated HIGH point and wrote config %s" % args.configfile
            
            
            

