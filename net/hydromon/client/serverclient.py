'''
Created on May 8, 2015

@author: markos
'''
import json
import logging
import requests

from net.hydromon.config import ConfigurationUtil
import os
from requests.exceptions import ConnectionError

log = logging.getLogger(__name__)
def send(valuedto):
    print "Sending data"
    payload = json.dumps(valuedto, default=serialize_valuedto, indent=2)
    endpointUrl = ConfigurationUtil.getAddValueEndpointUrl(valuedto.sensorId)
    log.debug("Sending data: " + payload + " to " + endpointUrl)
    response = None
    
    try:
        response = requests.post(endpointUrl, payload, timeout=10)
    except ConnectionError as ce:
        log.fatal(ce)
    finally:
        if response is not None:
            log.debug(response)
            if response.status_code != 200:
                log.warn("Received response code %s " % response.status_code)
                handleError(valuedto)
        else:
            handleError(valuedto) 
            
        
        
def serialize_valuedto(o):
    res = o.__dict__.copy()
    del res['sensorId']
    return res

def handleError(valuedto):
    ':type valuedto: net.hydromon.dto.valuedto'
    savedir = ConfigurationUtil.getEmergencySaveDirectoryForSensor(valuedto.sensorId)
    if not os.path.exists(savedir):
        os.mkdir(savedir)
        
    if not os.access(savedir, os.W_OK):
        log.error("Unable to write emergency data in %s" % savedir)
        return
    
    filename = savedir + "/sensordata_" + str(valuedto.time) + ".json" 
    payload = json.dumps(valuedto, default=serialize_valuedto, indent=2)
    
    f = open(filename, 'w')
    f.write(payload)
    f.flush() 
    f.close()
    log.warn("Wrote recovery data file %s " % filename)

if __name__ == '__main__':
    pass