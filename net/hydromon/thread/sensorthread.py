'''
Created on May 7, 2015

@author: markos
'''
import threading
import thread
import time
import logging

from net.hydromon.config import ConfigurationUtil
from net.hydromon.dto.valuedto import ValueDTO

log = logging.getLogger(__name__)

class SensorThread(threading.Thread):
    '''
    classdocs
    '''
    threadId = None
    module = None
    value = None
    timestamp = None
    exitFlag = False
    readInterval = None
    
    def __init__(self, threadId, module, readInterval):
        ':type module: net.hydromon.module.ModulePrototype'
        
        threading.Thread.__init__(self)
        self.threadId=threadId
        self.module=module
        self.readInterval=readInterval
    
    def run(self):
        
        while True:
            log.debug("Thread %s %s running" % (self.threadId, self.module))
            if (self.exitFlag):
                thread.exit()
            
            self.value=self.module.read()
            # self.timestamp=datetime.datetime.now(pytz.timezone('Europe/Helsinki')).isoformat()
            self.timestamp=time.time()*1000
            time.sleep(float(self.readInterval))
            
            
    def stop(self):
        self.exitFlag=True
        
        
    def getValue(self):
        return ValueDTO(self.module.sensorId, self.value, self.timestamp, ConfigurationUtil.HYDROMON_USERNAME, ConfigurationUtil.HYDROMON_APIKEY)
        
    def reset(self):
        self.value = None
        self.timestamp = None
        