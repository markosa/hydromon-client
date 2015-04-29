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
    

    def __init__(self, sensorId, module):
        '''
        Constructor
        '''
        self.sensorId=sensorId
        self.module=module
   
    def __repr__(self):
        return "Sensor (sensorId = %s, module = %s)" % (self.sensorId, self.module)
    
