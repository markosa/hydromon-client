'''
Created on Jul 1, 2015

@author: markos
'''

import HCSR04 as hc

if __name__ == '__main__':
    ''' trigger, echo '''
    val = hc.readvalue(23,24)
    val = val / 1000000.00
    
    distance = val * 343.59 * 100
    distance = distance / 2
    distance = distance / 1000000.00
    distance = round(distance, 2)
    print "Distance : %.1f" % distance    
    