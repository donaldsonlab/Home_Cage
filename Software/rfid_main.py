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

def rfidTrack_1(event1):
    #Set the event value to false
    event1.clear()

    #Defines the serial port and the binary data stream characteristics
    serial_1 = serial.Serial(
        port = '/dev/serial0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    while True:
        print("start1\n")
        line_1 = serial_1.readline()
        if vole_1 in line_1.decode(): 
            voleTags.put(["vole_1","1"])
            print(line_1.decode())
            tag = voleTags.get()
            voleTags.task_done()
            print(tag)
        if vole_2 in line_1.decode():
            voleTags.put(["vole_2","1"])
            print(line_1.decode())
            tag = voleTags.get()
            voleTags.task_done()
            print(tag)
        
#        if KeyboardInterrupt:
#            atexit.register(end)
#            print("RFID 1")
#            print("Queue")
#            print(list(voleTags.queue))
#            print("")
        #This block of code waits until all threads are finished running to move on
        print("beginCheck1\n")
        event1.set() #Indicate that the thread is complete
        mainEvent.wait()
        print("complete1\n")

def rfidTrack_2(event2):
    event2.clear()
    serial_2 = serial.Serial(
        port = '/dev/ttySC0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    while True:
        print("start2\n")
        line_2 = serial_2.readline()
        if vole_1 in line_2.decode(): 
            voleTags.put(["vole_1","2"])
            print(line_2.decode())
            tag = voleTags.get()
            voleTags.task_done()
            print(tag)
        if vole_2 in line_2.decode():
            voleTags.put(["vole_2","2"])
            print(line_2.decode())
            tag = voleTags.get()
            voleTags.task_done()
            print(tag)
        
#        if KeyboardInterrupt:
#            atexit.register(end)
#            print("RFID 1")
#            print("Queue")
#            print(list(voleTags.queue))
#            print("")
        #This block of code waits until all threads are finished running to move on
        print("beginCheck2\n")
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

    serial_1.close()
    serial_2.close()
    print("Finished \n")
    print(list(voleTags.queue))

if __name__ == '__main__':
    event1    = threading.Event()
    event2    = threading.Event()
    mainEvent = threading.Event()

    #Creates the threads that track RFID movements
    serial1 = threading.Thread(target = rfidTrack_1, args=(event1,))
    serial2 = threading.Thread(target = rfidTrack_2, args=(event2,))
    track   = threading.Thread(target = threadTrack, args=(event1,event2,))

    serial1.start()
    serial2.start()
    track.start()