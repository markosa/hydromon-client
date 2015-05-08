'''
Created on May 7, 2015

@author: markos
'''
import threading
import thread
import time
import logging

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
            self.timestamp=time.time()
            time.sleep(self.readInterval)
            
            
    def stop(self):
        self.exitFlag=True
        
        
        
        
        
        