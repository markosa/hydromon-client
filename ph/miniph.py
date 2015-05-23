'''
Created on May 22, 2015

@author: Marko Sahlman
'''

try:
    import smbus
except:
    print "error"
    
import ConfigParser
import argparse
import os
import sys

class MiniPH(object):
    '''
    classdocs
    
    This file is almost 1:1 copied & converted from Sparky's portfolio. 
    
    http://www.sparkyswidgets.com/portfolio-item/miniph-i2c-ph-interface/
    
    '''
    pH4Cal = 1286
    pH7Cal = 2048
   
    def __init__(self, address,smbusid=1, vref=3.3, opampGain=5.25):
        '''
        Constructor
        '''
        self.smbusid=smbusid
        self.address=address
        self.vref=vref
        self.bus=smbus.SMBus(smbusid)
        self.opampGain=opampGain
    
    def readRawValue(self):
        data = self.bus.read_i2c_block_data(int(self.address,16), 1,2)
        high = data[0]
        low = data[1]
        adc_result = (high * 256) + low
        return adc_result

    def calibratePH4(self):
        self.pH4Cal=self.readRawValue()
        self.calculateSlope()
    
    def calibratePH7(self):
        self.pH7Cal=self.readRawValue()
        self.calculateSlope()
    
    def calculateSlope(self):
        self.pHStep = ((((self.vref*(float)(self.pH7Cal - self.pH4Cal))/4096.0)*1000)/self.opampGain)/3
        return self.pHStep
        
    def calcPH(self,raw):
        miliVolts = ((raw/4096.0)*self.vref)*1000 
        temp = ((((self.vref*self.pH7Cal)/4096.0)*1000)- miliVolts)/self.opampGain
        pH = 7-(temp/self.pHStep)
        return pH

    def readPH(self):
        return self.calcPH(self.readRawValue())

    def writeConfig(self,configfile):
        config = ConfigParser.RawConfigParser()
        configsection = "miniph_%s" % self.address 
        config.add_section(configsection)
        ''' smbusid=1, address=0x4d, vref=3.3, opampGain=5.25 '''
        config.set(configsection, 'smbusid', self.smbusid)
        config.set(configsection, 'address', self.address)
        config.set(configsection, 'opampGain', self.opampGain)
        config.set(configsection, 'pH4Cal', self.pH4Cal)
        config.set(configsection, 'pH7Cal', self.pH7Cal)
        config.set(configsection, 'pHStep', self.pHStep)
        config.set(configsection, 'vref', self.vref)

        with open(configfile, 'wb') as configfile:
            config.write(configfile)
        
    
    def readConfig(self,configfile):
        config = ConfigParser.RawConfigParser()

        configsection = "miniph_%s" % self.address 
        config.read(configfile)
        self.smbusid = config.get(configsection, 'smbusid')
        self.address = config.get(configsection, 'address')
        self.opampGain = float(config.get(configsection, 'opampGain'))
        self.pH4Cal = int(config.get(configsection, 'pH4Cal'))
        self.pH7Cal = int(config.get(configsection, 'pH7Cal'))
        self.pHStep = float(config.get(configsection, 'pHStep'))
        self.vref = float(config.get(configsection,'vref'))


def interactiveCalibration():
    print "** CALIBRATION **"
    
    
    raw_input("1. Put sensor in PH7 solution and press enter to calibrate")
    raw_input("2. Clean sensor and put sensor in PH4 solution and press enter to calibrate")
  
        
    pass

if __name__ == '__main__':
    
    interactiveCalibration()
    
    parser = argparse.ArgumentParser(description='Read or calibrate ph probe. Calibrate using --ph4 and --ph7 flags. Put probe in ph7 solution and use flag --ph7 then change probe to ph4 solution and use --ph4')
    parser.add_argument('busid', metavar='BUSID', type=int, nargs='?',help='I2C bus id. Ie. 0 or 1')    
    parser.add_argument('address', metavar='ADDRESS', type=str, nargs='?',help='I2C Address. Ie. 0x4d')    

    parser.add_argument('--configfile', help='config file')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--ph4', action='store_true')
    group.add_argument('--ph7', action='store_true')
    
    args = parser.parse_args()  
    
    if  not args.address or not args.busid:
            parser.print_usage()
            sys.exit(1)
            
    if not args.ph4 and not args.ph7:
        if args.configfile and os.path.exists(args.configfile):
            phi2c = MiniPH(args.address, args.busid)
            phi2c.readConfig(args.configfile)
            print str(phi2c.readPH())
        else:
            parser.print_usage()
            print "\nError: no config file given or it does not exist. Calibrate and save config or give new config file location"
            sys.exit(1)

    elif args.ph4:
            phi2c = MiniPH(args.address, args.busid)
            if os.path.exists(args.configfile):
                phi2c.readConfig(args.configfile)
            phi2c.calibratePH4()
            phi2c.writeConfig(args.configfile)
            print "Calibrated PH4 point and wrote config %s" & args.configfile
    elif args.ph7:
            phi2c = MiniPH(args.address, args.busid)
            if os.path.exists(args.configfile):
                phi2c.readConfig(args.configfile)
            phi2c.calibratePH7()
            phi2c.writeConfig(args.configfile)        
            print "Calibrated PH7 point and wrote config %s" & args.configfile
            
            
            

