'''
Created on Apr 28, 2015

@author: markos
'''
from ConfigParser import ConfigParser
import logging
from net.hydromon.dto.sensordto import Sensor

log = logging.getLogger(__name__)

HYDROMON_USERNAME = None
HYDROMON_APIKEY = None
HYDROMON_SERVER = None

SENSORS = []

def readConfiguration():
    config = ConfigParser()
    config.read('conf/sensors.conf')
    log.debug('Parsed configuration')
    log.debug(config.sections())
    parseCommon(config)
    parseSensors(config)
    return config
    
    
def parseSensors(config):
    for section in config.sections():
        if section.startswith('sensor_'):
            parseSensor(config, section)
    
def parseSensor(config, section):
    global SENSORS
    SENSORS.append(Sensor(config.get(section, 'id'), config.get(section, 'module')))


def parseCommon(config):
    global HYDROMON_USERNAME, HYDROMON_APIKEY, HYDROMON_SERVER 
    HYDROMON_USERNAME = config.get('common', 'username')
    HYDROMON_APIKEY = config.get('common', 'apikey')
    HYDROMON_SERVER = config.get('common', 'hydromon-server')
    

