'''
Created on May 6, 2015

@author: markos
'''

import net.hydromon.dto.sensordto  # @UnusedImport
import logging
import time

log = logging.getLogger(__name__)

try:
    import Adafruit_DHT
except:
    log.fatal("Adafruit DHT library is missing")


DEVICE_BASE_DIR='/sys/bus/w1/devices'

class AM2302():
    '''
    classdocs
   
    Read logic copied from this article
    https://learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf
    
    '''
    serial = None
    device = None 
    sensorId = None
    gpio_pin = None
    sensor_args = { '11': Adafruit_DHT.DHT11,
                                '22': Adafruit_DHT.DHT22,
                                '2302': Adafruit_DHT.AM2302 }
    def __init__(self, sensor):
        ':type sensor: net.hydromon.dto.sensordto.Sensor'
        self.serial=sensor.serial
        self.sensorId=sensor.sensorId
        self.gpio_pin=sensor.gpio_pin
        
    def testConfig(self):
        #self.read()
        pass
     
        
    def read(self):
        sensor = self.sensor_args['2302']
        
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.gpio_pin)
        if humidity is not None and temperature is not None:
            log.debug('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
            return '{0:0.1f}'.format(humidity)
        
        return '0'

    