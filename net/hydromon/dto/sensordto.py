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

    def __init__(self, sensorId, module, gpio_pin, serial):
        '''
        Constructor
        '''
        self.sensorId=sensorId
        self.module=module
        self.gpio_pin=gpio_pin
        self.serial=serial
   
    def __repr__(self):
        return "Sensor (sensorId = %s, module = %s, gpio_pin = %s, serial = %s)" % (self.sensorId, self.module, self.gpio_pin, self.serial)
    
