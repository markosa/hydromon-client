'''
Created on Apr 28, 2015

@author: markos
'''
from ConfigParser import ConfigParser, NoOptionError
import logging
from net.hydromon.dto.sensordto import Sensor

log = logging.getLogger(__name__)

HYDROMON_USERNAME = None
HYDROMON_APIKEY = None
HYDROMON_SERVER = None
READ_INTERVAL = 60
DATADIR = None

SENSORS = []

def readConfiguration():
    try:
        config = ConfigParser()
        config.read('conf/sensors.conf')
        log.debug('Parsed configuration')
        log.debug(config.sections())
        parseCommon(config)
        parseSensors(config)
    except NoOptionError as noe:
        log.error("Configuration error %s" % noe)
        raise
    
    return config
    
    
def parseSensors(config):
    for section in config.sections():
        if section.startswith('sensor_'):
            parseSensor(config, section)
     
def parseSensor(config, section):
    global SENSORS
    SENSORS.append(Sensor(config.get(section, 'id'), config.get(section, 'module'), config.get(section,'gpio_pin'), config.get(section,'serial')))


def parseCommon(config):
    global HYDROMON_USERNAME, HYDROMON_APIKEY, HYDROMON_SERVER, DATADIR
    HYDROMON_USERNAME = config.get('common', 'username')
    HYDROMON_APIKEY = config.get('common', 'apikey')
    HYDROMON_SERVER = config.get('common', 'hydromon-server')
    DATADIR = config.get('common', 'data-dir')

   
def getAddValueEndpointUrl(sensorId):
    return HYDROMON_SERVER+"/api/sensor/%s/addvalue" % sensorId     

def getEmergencySaveDirectoryForSensor(sensorId):
    return DATADIR + "/sensor_%s" % sensorId
