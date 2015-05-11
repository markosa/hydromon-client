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

log = logging.getLogger(__name__)

MODULE_INSTANCES = []
THREADS = []

def setupLogging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
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
            sys.exit(4)

def spawnThreads():
    for module in MODULE_INSTANCES:
        ': :type module: net.hydromon.module.prototype.ModulePrototype'
        t = SensorThread("SensorThread #"+module.sensorId, module, ConfigurationUtil.READ_INTERVAL)
        t.start()
        log.info("Spawned thread: " + str(t))
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


def main():   
    loadModules()
    spawnThreads()
    testVar = raw_input("Ask user for something.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--flush', action='store_true')
    args = parser.parse_args()
    
    config = setup()  # @UnusedVariable

    
    if args.flush:
        print "foo"
        flush.flush()
    else:
        main()