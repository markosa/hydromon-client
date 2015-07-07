'''
Created on May 22, 2015

@author: markos
'''


if __name__ == '__main__':
    ecLowCal = 50.00
    ecHighCal = 119.00
    ecLowCalValue = 0.00
    ecHighCalValue = 1413.00
    ecCalTemp = 22.0
    
    offset = ecLowCal
    ec_raw_delta = ecHighCal - ecLowCal
    
    ec_delta = ecHighCalValue - ecLowCalValue
    
    ecStep = ec_delta / ec_raw_delta
    
    print ecStep
    
    measuredValue1 = 50
    measuredValue2 = 119
    measuredValue3 = 70
    
    ec1 = (measuredValue1-offset) * ecStep
    ec2 = (measuredValue2-offset) * ecStep
    ec3 = (measuredValue3-offset) * ecStep
    
    print ec1
    print ec2
    print ec3
    
    
    
    
    
    