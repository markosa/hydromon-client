'''
Created on May 19, 2015

@author: markos
'''

class SensorTimedOutError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)
        