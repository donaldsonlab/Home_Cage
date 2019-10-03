#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron & Katara Ziegler
# Date Edited: 9-26-19
# Description: This script is a test for the threading concept I am trying to
#              implement. Mostly I want to test how the synchronization scheme I am 
#              trying to get working. 
#####################################################################################

import serial
import threading
import time
#import Queue as queue # for terminal
import queue # for Thonny
import atexit
import random

vole_1 = "72C526" # Strings defining the ID of the voles, change according to vole RFID tags
vole_2 = "736C8E"

voleTags = queue.LifoQueue() #Initialize a LIFO (last-in first-out) queue to share with the other process?. Might not be the way to do this
timeQueue = queue.LifoQueue() #Not sure about this one, we'll see how I want to structure this variable
timeQueue.put(0) #Initialize the Queue with a value of zero
numThreads = 2 #Number of threads to be running

def rfidTrack_1(event):
    #Set the event to false and wait at the end
    event1.clear()

    print("begin1\n")
    #Defines the serial port and the binary data stream characteristics
    #serial_1 = serial.Serial(
    #    port = '/dev/serial0',
    #    baudrate = 9600,
    #    parity = serial.PARITY_NONE,
    #    bytesize = serial.EIGHTBITS,
    #    timeout = 1
    #)

    #this is the continuous loop that runs on the Pi waiting for an RFID ping. 
    while True:
        threadNum = 0
        print("startRead1\n")
        rand_1 = random.randint(1,50)
        if rand_1 == 1:  #Simulated vole1 ping
            voleTags.put(["vole_1","1"])
        else:
            voleTags.put(["none","1"])
        if rand_1 == 2: #Simulated vole2 ping
            voleTags.put(["vole_2","1"])
        else:
            voleTags.put(["none","1"])
        
#        if KeyboardInterrupt:
#            atexit.register(end)
#            print("RFID 1")
#            print("Queue")
#            print(list(voleTags.queue))
#            print("")
        #This block of code waits until all threads are finished running to move on
        print("beginCheck1\n")
        #threadNum = timeQueue.get(timeout=1) #Read the value of the syncronization queue
        #timeQueue.task_done()
        #threadNum = threadNum + 1 #increment the check condition no matter what
        #timeQueue.put(threadNum)
        #while (threadNum < numThreads) & (threadNum != 0): #If this this thread isn't the last to complete
        #    print("not_complete1\n")
        #    threadNum = timeQueue.get()
        #    timeQueue.task_done()
        #    #PUT SOME VALUE BACK IN THE QUEUE TO AVOID EMPTY QUEUE
        #    timeQueue.put(threadNum)
        #threadNum = 0
        #timeQueue.put(threadNum) #Re-initialize the check condition

        event1.set()
        mainEvent.wait()
        print("complete1\n")
        #STILL SOME LAG WHEN PYTHON IS SWITCHING BETWEEN THE TWO THREADS. IS THIS STILL APPLICABLE IF 
        #WE USE A REAL THREADING INTERPRETER?
def rfidTrack_2(event):
    #Set initial event to flase
    event2.clear()

    print("begin2\n")
    #serial_2 = serial.Serial(
    #    port = '/dev/ttySC0',
    #    baudrate = 9600,
    #    parity = serial.PARITY_NONE,
    #    bytesize = serial.EIGHTBITS,
    #    timeout = 1
    #)

    while True:
        threadNum = 0
        print("startRead2\n")
        rand_2 = random.randint(1,50)
        if rand_2 == 1: 
            voleTags.put(["vole_1","2"])
        else:
            voleTags.put(["none","2"])
        if rand_2 == 2:
            voleTags.put(["vole_2","2"])
        else:
            voleTags.put(["none","2"])
        
#        if KeyboardInterrupt:
#            atexit.register(end)
#            print("RFID 1")
#            print("Queue")
#            print(list(voleTags.queue))
#            print("")
        #This block of code waits until all threads are finished running to move on
        print("beginCheck2\n")
        #threadNum = timeQueue.get(timeout=1) #Read the value of the syncronization queue
        #timeQueue.task_done()
        #threadNum = threadNum + 1 #increment the check condition no matter what
        #timeQueue.put(threadNum)
        #while (threadNum < numThreads) & (threadNum != 0): #If this this thread isn't the last to complete
        #    print("not_complete2\n")
        #    threadNum = timeQueue.get()
        #    timeQueue.task_done()
        #    timeQueue.put(threadNum)
        #threadNum = 0
        #timeQueue.put(threadNum) #Re-initialize the check condition

        event2.set()
        mainEvent.wait()
        print("complete2\n")


def threadTrack(event1,event2):
    while True:
        mainEvent.clear()

        event1.wait()
        event2.wait()

        mainEvent.set()

def end():
    serial1.join()
    serial2.join()

    #serial_1.close()
    #serial_2.close()
    print("Finished \n")
    print(list(voleTags.queue))

if __name__ == '__main__':
    mainEvent = threading.Event()
    event1    = threading.Event()
    event2    = threading.Event()

    #Creates the threads that track RFID movements
    serial1 = threading.Thread(target = rfidTrack_1, args=(event1,))
    serial2 = threading.Thread(target = rfidTrack_2, args=(event2,))
    track   = threading.Thread(target = threadTrack, args=(event1,event2,))

    serial1.start()
    serial2.start()
    track.start()