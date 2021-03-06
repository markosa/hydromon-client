'''
Created on Apr 27, 2015

@author: markos
'''
import logging
import sys
import os
from net.hydromon.config import ConfigurationUtil
from ConfigParser import NoOptionError
from net.hydromon.dto.sensordto import Sensor # @UnusedImport
from net.hydromon.module.prototype import ModulePrototype # @UnusedImport
from net.hydromon.thread.sensorthread import SensorThread
from net.hydromon.thread.readerthread import ReaderThread
import argparse
from net.hydromon.flush import flush
import traceback
import time
from datetime import datetime
import signal

log = logging.getLogger(__name__)

MODULE_INSTANCES = []
THREADS = []

def setupLogging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.INFO)
    
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    root.addHandler(ch)
    root.addHandler(fh)
    
    logging.getLogger("requests").setLevel(logging.WARNING)

    
def setup():
    setupLogging()
    log.info("Setting up hydromond client") 
    config = None
    try:
        config = ConfigurationUtil.readConfiguration()
    except NoOptionError as noe:
        log.error(noe)
        sys.exit(1)
    except:
        log.error("Unexpected error:", sys.exc_info()[0])
        sys.exit(2)

    initializeDatadirectory()

    log.info("Initializing sensors: "  + str(ConfigurationUtil.SENSORS))
    return config


def loadModules():
    for sensor in ConfigurationUtil.SENSORS:
        ': :type sensor: net.hydromon.dto.sensordto.Sensor'
        try:
            module = __import__("net.hydromon.module.%s" % sensor.module, fromlist=["net.hydromon.module"])
            clazz = getattr(module,sensor.module)
            instance = clazz(sensor)

            instance.testConfig()
            
            MODULE_INSTANCES.append(instance)
            log.info("Module %s loaded" % instance)
        except AttributeError as ae:
            log.error("Invalid module in Sensor #%s:%s => %s" % (sensor.sensorId, sensor.module, ae) )
            sys.exit(3)
        except:
            log.error("Error in loading module %s" % sensor.module)
            log.error("Error:", sys.exc_info()[0])
            log.error("Error:", sys.exc_info())
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            sys.exit(4)

def spawnThreads():
    for module in MODULE_INSTANCES:
        ': :type module: net.hydromon.module.prototype.ModulePrototype'
        t = SensorThread("SensorThread #"+module.sensorId, module, ConfigurationUtil.READ_INTERVAL)
        t.start()
        log.info("Spawned thread: " + str(t))
        time.sleep(2)
        THREADS.append(t)
        
    readerThread = ReaderThread("Reader#1", THREADS, ConfigurationUtil.SEND_INTERVAL)
    readerThread.start()
    
def initializeDatadirectory():
    if not os.path.exists(ConfigurationUtil.DATADIR):
        os.mkdir(ConfigurationUtil.DATADIR)
        
    log.info("Using %s as data directory" % ConfigurationUtil.DATADIR)
    
    if not os.access(ConfigurationUtil.DATADIR, os.W_OK):
        log.error("%s is not writable")
        sys.exit(5)

def handler(signum, frame):
    printStatistics()
    
def printStatistics():
    log.info("** Statistics **")
    for t in THREADS:
        ': :type t: net.hydromon.thread.sensorthread.SensorThread'
        log.info("%s#%s: %s" % (str(t.module.__class__), str(t.module.sensorId), str(t.value)))

def main():   
    loadModules()
    spawnThreads()
    log.info("Registering signal.SIGALRM - Use for statistics")
    signal.signal(signal.SIGALRM, handler)
    
    while True:
        if datetime.now().minute == 0:
            printStatistics()
        
        time.sleep(float(60))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--flush', action='store_true')
    args = parser.parse_args()
    
    config = setup()  # @UnusedVariable

    
    if args.flush:
        flush.flush()
    else:
        main()