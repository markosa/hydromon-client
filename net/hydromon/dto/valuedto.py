'''
Created on Apr 23, 2015

@author: markos
'''

class ValueDTO():
    
    sensorId = None
    value = None
    time = None
    apikey = None
    uid = None

    def __init__(self, sensorId, value, time, uid, apikey):
        self.sensorId=sensorId
        self.value=value
        self.time=time
        self.uid=uid
        self.apikey=apikey

        