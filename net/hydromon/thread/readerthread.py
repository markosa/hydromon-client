''''
Created on May 7, 2015

@author: markos
'''
import threading
import thread
import time
import logging

from net.hydromon.client import serverclient

log = logging.getLogger(__name__)

class ReaderThread(threading.Thread):
    '''
    classdocs
    '''

    threadId = None
    readInterval = None
    exitFlag = False
    threads = []
    
    def __init__(self, threadId, threads, readInterval):
        threading.Thread.__init__(self)
        self.threadId=threadId
        self.readInterval=readInterval
        self.threads=threads
    
    def run(self):
        
        while True:
            log.debug("** ReaderThread %s running" % (self.threadId))
            if (self.exitFlag):
                log.fatal("Received exit notification")
                thread.exit()
            
            log.debug("Threads to run: " + str(len(self.threads)))
            
            for t in self.threads:
                ': :type t: net.hydromon.thread.sensorthread.SensorThread'
                if t.timestamp is not None:
                    valueDto = t.getValue()
                    serverclient.send(valueDto)
                else:
                    log.debug("Thread has not yet processed any data: " + str(t))
            
            time.sleep(float(self.readInterval))
            
            
        log.fatal("Thread GONE")
            
            
    def stop(self):
        self.exitFlag=True
        
        