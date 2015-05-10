'''
Created on May 10, 2015

@author: markos
'''

import os
from net.hydromon.config import ConfigurationUtil
import glob
import requests
import logging
from requests.exceptions import ConnectionError
log = logging.getLogger(__name__)

def flush():
    for sensor in ConfigurationUtil.SENSORS:
        ': :type sensor: net.hydromon.dto.sensordto.Sensor'
        sensorDataDir =  ConfigurationUtil.getEmergencySaveDirectoryForSensor(sensor.sensorId)
        
        if os.path.exists(sensorDataDir):
            log.info("Flushing " + sensorDataDir)
            files = glob.glob(sensorDataDir+"/sensordata*.json")
            endpointUrl = ConfigurationUtil.getAddValueEndpointUrl(sensor.sensorId)

            for datafile in files: 
                log.info("Sending file " + datafile)
                f = open(datafile, 'rw')
                payload = f.read()
                
                log.debug("Sending data: " + payload + " to " + endpointUrl)
                response = None
                
                try:
                    response = requests.post(endpointUrl, payload)
                except ConnectionError as ce:
                    log.fatal(ce)
                finally:
                    if response is not None:
                        log.debug(response)
                        if response.status_code != 200:
                            log.error("Received response code %s " % response.status_code)
                        else:
                            os.remove(datafile)
                    else:
                        log.error("Unable to flush file to server.")



if __name__ == '__main__':
    pass