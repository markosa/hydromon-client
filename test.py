'''
Created on Apr 23, 2015

@author: markos
'''

from net.hydromon.sensorvalue import SensorValue 

if __name__ == '__main__':
    dto = SensorValue("foobar")
    dto2 = SensorValue("foobar2")
    dto.test="foobar bar"
    print dto.test
    
    
    
    
    
    