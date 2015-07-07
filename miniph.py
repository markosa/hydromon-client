'''
Created on May 22, 2015

@author: markos
'''
import smbus
import time

bus = smbus.SMBus(1)
address = 0x4d
vRef = 3.3
opampGain = 5.25

pH4Cal = 2268
pH7Cal = 2044
pHStep = 1


def readvalue():
    data = bus.read_i2c_block_data(address, 1,2)
    print data
    high = data[0]
    low = data[1]
    adc_result = (high * 256) + low
    return adc_result


def calcpH(raw):
    miliVolts = ((raw/4096.0)*vRef)*1000
    temp = ((((vRef*pH7Cal)/4096.0)*1000)- miliVolts)/opampGain
    pH = 7-(temp/pHStep)
    return pH
 

if __name__ == '__main__':
        adc_result = readvalue()
        print "adc: " + str(adc_result)
        pHStep = ((((vRef*(float)(pH7Cal - pH4Cal))/4096.0)*1000)/opampGain)/3
        ph = calcpH(adc_result)
        print "ph:"+str(ph)