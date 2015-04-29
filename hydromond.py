'''
Created on Apr 27, 2015

@author: markos
'''
import logging
import sys
from net.hydromon.config import ConfigurationUtil

log = logging.getLogger(__name__)

sensors = []

def setupLogging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
def setup():
    setupLogging()
    log.info("Setting up hydromond client") 
    return ConfigurationUtil.readConfiguration()


def main():   
    config = setup()  # @UnusedVariable


if __name__ == '__main__':
    main()