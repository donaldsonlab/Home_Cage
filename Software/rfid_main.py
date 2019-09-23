#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron & Katara Ziegler
# Date Edited: 9-20-19
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

vole_1 = "72C526" # Strings defining the ID of the voles, change according to vole RFID tags
vole_2 = "736C8E"

voleTags = queue.LifoQueue() #Initialize a LIFO (last-in first-out) queue to share with the other process?. Might not be the way to do this
timeQueue = queue.LifoQueue() #Not sure about this one, we'll see how I want to structure this variable
timeQueue.put(0) #Initialize the Queue with a value of zero
numThreads = 2 #Number of threads to be running

def rfidTrack_1():
    print("begin1")
    threadNum = 0;
    #Defines the serial port and the binary data stream characteristics
    serial_1 = serial.Serial(
        port = '/dev/serial0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    while True:
        print("istrue1")
        line_1 = serial_1.readline()
        if vole_1 in line_1.decode(): 
            voleTage.put("vole_1,1")
        if vole_2 in line_1.decode():
            voleTags.put("vole_2,1")
        
#        if KeyboardInterrupt:
#            atexit.register(end)
#            print("RFID 1")
#            print("Queue")
#            print(list(voleTags.queue))
#            print("")
        #This block of code waits until all threads are finished running to move on
        print("beginCheck1")
        threadNum = timeQueue.get()
        threadNum = threadNum + 1
        timeQueue.put(threadNum)
        timeQueue.task_done()
        print(threadNum)
        print("Initial_1")
        while threadNum < numThreads:
            threadNum = timeQueue.get()
            print(threadNum)
            print("rfid_1")
            timeQueue.task_done()

    #Include some wait condition for the other threads to end as well
def rfidTrack_2():
    print("begin2")
    threadNum = 0
    serial_2 = serial.Serial(
        port = '/dev/ttySC0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    while True:
        print("istrue2")
        line_2 = serial_2.readline()
        if vole_1 in line_2.decode(): 
            voleTags.put("vole_1,1")
        if vole_2 in line_2.decode():
            voleTags.put("vole_2,1")
        
#        if KeyboardInterrupt:
#            atexit.register(end)
#            print("RFID 1")
#            print("Queue")
#            print(list(voleTags.queue))
#            print("")
        #This block of code waits until all threads are finished running to move on
        print("beginCheck2")
        print(timeQueue.get())
        threadNum = timeQueue.get()
        print("midcheck2")
        threadNum = threadNum + 1
        print("midcheck2")
        timeQueue.put(threadNum)
        print(threadNum)
        print("Initial_2")
        timeQueue.task_done()
        while threadNum < numThreads:
            threadNum = timeQueue.get()
            print(threadNum)
            print("rfid_2")
            timeQueue.task_done()

def end():
    serial1.join()
    serial2.join()

    serial_1.close()
    serial_2.close()
    print("Finished \n")
    print(list(voleTags.queue))

if __name__ == '__main__':
    #Creates the threads that track RFID movements
    serial1 = threading.Thread(target = rfidTrack_1)
    serial2 = threading.Thread(target = rfidTrack_2)

    serial1.start()
    serial2.start()