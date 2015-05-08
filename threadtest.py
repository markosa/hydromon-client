'''
Created on Apr 27, 2015

@author: markos
'''
from time import sleep
import threading
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

log = logging.getLogger(__name__)

def init():
    stopEvent = threading.Event()
    t1 = threading.Thread(target=readProbesThread,args=(1,stopEvent))
    t1.start()
    sleep(60)
    stopEvent.set()


def readProbesThread(arg1, stop_event):
    print "t"
    while(not stop_event.is_set()):
        print "foobar"
        sleep(10)


if __name__ == '__main__':
    log.info("test")
