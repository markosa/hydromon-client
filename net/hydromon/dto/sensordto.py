'''
Created on Apr 28, 2015

@author: markos
'''

class Sensor(object):
    '''
    classdocs
    '''
    sensorId = None
    module = None
    gpio_pin = None
    serial = None
    moduleOptions = None

    def __init__(self, sensorId, module, gpio_pin, serial, moduleOptions):
        '''
        Constructor
        '''
        self.sensorId=sensorId
        self.module=module
        self.gpio_pin=gpio_pin
        self.serial=serial
        self.moduleOptions=moduleOptions
   
    def __repr__(self):
        return "Sensor (sensorId = %s, module = %s, gpio_pin = %s, serial = %s, moduleOptions = %s)" % (self.sensorId, self.module, self.gpio_pin, self.serial, self.moduleOptions)
    
