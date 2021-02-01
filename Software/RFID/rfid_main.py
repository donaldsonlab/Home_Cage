#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron & Katara Ziegler
# Date Edited: 10-31-19
# Description: This process will include 4 separate and individual threads that each 
#              control a separate RFID chip. Each thread runs the exact same 
#              instructions, and each thread will only start again once all threads
#              have completed so as to synchronize the timing.
#####################################################################################

import serial
import threading
import time
#import Queue as queue # for terminal
import queue # for Thonny
import atexit
import multiprocessing as mp 

#Create vole class that stores all the necessary info for each vole
class voleClass:
    def __init__(self, ping1 = None, ping2 = None, transition = None, pos = None):
        self.ping1      = ping1
        self.ping2      = ping2
        self.transition = transition
        self.pos        = pos

class tracker:
    def __init__(self, mainEvent = None, event1 = None, event2 = None, voleTag1 = None, voleComm1 = None, voleTag2 = None, voleComm2 = None):
        self.mainEvent = mainEvent
        self.event1    = event1
        self.event2    = event2
        self.voleTag1  = voleTag1
        self.voleTag2  = voleTag2
        self.voleComm1 = voleComm1
        self.voleComm2 = voleComm2

    def set_variables(self, eventDict, voleDict):
        # SET_VARIABLES sets the necessary tracking variables within the object

        #Pull the event variables out
        self.mainEvent = eventDict.get("mainEvent")
        self.event1    = eventDict.get("event1")
        self.event2    = eventDict.get("event2")

        #Pull the vole variables out
        self.voleTag1   = voleDict.get("voleTag1")
        self.voleComm1  = voleDict.get("vole1")
        self.voleTag2   = voleDict.get("voleTag2")
        self.voleComm2  = voleDict.get("vole2")
        
    def track_event(self, eventNum, serialPort):
        # TRACK_EVENT is the function that tracks the vole according to the event given in the input
        # Inputs:   eventNum         - Integer that is the event number to maintain in this tracking function

        def tracker_switch(self, args):
            # TRACKER_SWITCH is a function that acts a switch statement to return the correct event to track
            #switcher = {
            #    1 : self.event1,
            #    2 : self.event2,
            #    3 : self.event3,
            #    4 : self.event4
            #}
            
            #return switcher.get(args, "Invalid Event Number")

            # Not ideal but an if statement
            if eventNum == 1:
                trackedEvent = self.event1
            elif eventNum == 2:
                trackedEvent = self.event2
            elif eventNum == 3:
                trackedEvent = self.event3
            elif eventNum == 4:
                trackedEvent = self.event4
            else:
                Warning("Invalid Event Number")

            return trackedEvent
        
        # Identify the correct event
        trackedEvent = self.tracker_switch(eventNum)
        while True:
            # Set the event value to false
            trackedEvent.clear()

            line_1 = serialPort.readline()
            if self.voleTag1 in line_1.decode():
                print('Vole 1 Ping')
                if self.voleComm1.transition == 0: #Entering transition
                    self.voleComm1.ping1 = 1 #RFID number of the ping
                    self.voleComm1.transition = 1 # In the transition state
                elif self.voleComm1.transition == 1: # Already in the transition state
                    self.voleComm1.ping2 = 1
                    print('Recieved Ping')
                
            if self.voleTag2 in line_1.decode():
                print('Vole 2 Ping')
                if self.voleComm2.transition == 0:
                    self.voleComm2.ping1 = 1
                    self.voleComm2.transition = 1
                elif self.voleComm2.transition == 1:
                    self.voleComm2.ping2 = 1
                    print('RFID Ping Recieved')
                    self.voleComm2.transition = 0
            
            # Indicate thread is complete and wait
            trackedEvent.set()
            self.mainEvent.wait()

def rfidTrack_1(eventDict,voleDict):
    #Defines the serial port and the binary data stream characteristics
    serial_1 = serial.Serial(
        port = '/dev/ttySC0', #serial0 for Pi port
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    # Set the tracker variables
    tracker1 = tracker()
    tracker1.set_variables(eventDict, voleDict)

    # Track the voles
    tracker1.track_event(1, serial_1)

def rfidTrack_2(eventDict,voleDict):
    serial_2 = serial.Serial(
        port = '/dev/ttySC1',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    # Set the tracker variables
    trackerVars = tracker()
    trackerVars.set_variables(eventDict, voleDict)

    # Track the event2
    trackerVars.track_event(2, serial_2)

def rfidTrack_3(eventDict,voleDict):
    serial_3 = serial.Serial(
        port = '/dev/ttySC2',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    # Set the tracker variables
    trackerVars = tracker()
    trackerVars.set_variables(eventDict, voleDict)

    # Track the event3
    trackerVars.track_event(3, serial_3)

def rfidTrack_4(eventDict,voleDict):
    serial_4 = serial.Serial(
        port = '/dev/ttySC3',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    # Set the tracker variables
    trackerVars = tracker()
    trackerVars.set_variables(eventDict, voleDict)

    # Track the event4
    trackerVars.track_event(4, serial_4)

def threadTrack(eventDict):
    mainEvent = eventDict.get("mainEvent")
    event1    = eventDict.get("event1")
    event2    = eventDict.get("event2")
    while True:
        mainEvent.clear()

        event1.wait()
        event2.wait()

        mainEvent.set()

def end():
    serial1.join()
    serial2.join()
    serial3.join()
    serial4.join()

    serial_1.close()
    serial_2.close()
    serial_3.close()
    serial_4.close()
    print("Finished \n")
    print(list(voleTags.queue))

########################################################################################################
def main(vole1, vole2):
    #voleComm is the proxy object that is created from the vole class. Anything changed in that object will be reflected in the Modular code (doors)
    voleTag1 = "71B050" #"72C526" # Strings defining the ID of the voles, change according to vole RFID tags
    voleTag2 = "98656C" #"736C8E"

    ## CREATE ALL QUEUES NECESSARY
    voleTags = queue.LifoQueue() #Initialize a LIFO (last-in first-out) queue to track all vole pings
    vole1Queue = queue.LifoQueue() #Initialize queue to share vole class
    vole2Queue = queue.LifoQueue()

    #Create vole class objects, THESE SHOULD BE PROXIES
    #vole1 = voleClass(transition=0) #Initialize transition state to 0
    #vole2 = voleClass(transition=0)
    vole1.transition = 0
    vole2.transition = 0

    #Create Dictionary for all of these vole related objects
    voleDict = {
        "voleTag1"    : voleTag1,
        "voleTag2"    : voleTag2,
        "vole1"     : vole1,
        "vole2"     : vole2,
    }
    ########################################################################################################

    #if __name__ == '__main__':
    event1    = threading.Event()
    event2    = threading.Event()
    event3    = threading.Event()
    event4    = threading.Event()
    mainEvent = threading.Event()
    eventDict = {
        "event1"   : event1,
        "event2"   : event2,
        "event3"   : event3,
        "event4"   : event4,
        "mainEvent": mainEvent
    }


    #Creates the threads that track RFID movements, each thread is for a different RFID tracker (total 4 in the end)
    serial1 = threading.Thread(name='serial1',target = rfidTrack_1, args=(eventDict,voleDict))
    serial2 = threading.Thread(name='serial2',target = rfidTrack_2, args=(eventDict,voleDict))
    serial3 = threading.Thread(name='serial3',target = rfidTrack_3, args=(eventDict,voleDict))
    serial4 = threading.Thread(name='serial4',target = rfidTrack_4, args=(eventDict,voleDict))
    track   = threading.Thread(name='tracking',target = threadTrack, args=(eventDict,)) # Tracking thread

    serial1.start()
    serial2.start()
    serial3.start()
    serial4.start()
    track.start()