#---------------------------------------------------------------------------------------------------
# This script tests simply the CAN bus connection between the arduino and the raspberry pi. This handles both the arduino sending through the pyfirmata library and the recieveing end on the pi through the pycan library. To start out, we simply send a known time dependent signal and see how accurate the output is. 
#---------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import matplotlib as plt
import pyfirmata as pf
import can # python-can
import serial
import time
import atexit

class cageChamber:
    # CAGECHAMBER is the base class for each chamber in the simulation
    def __init__(self,name = None,readers = [None], chambers = [None]):
        self.readers = readers
        self.chambers = chambers
        self.name = name

class rfidReader:
    # RFIDREADER is the base class for an rfid reader in the system
    def __init__(self, name = None, chamber = None):
        self.name = name
        self.chamber = chamber

    def passed(self, sendObj):
        # PASSED is the function that is called when a vole passes through the rfid reader. It will facilitate the sending of data to the Arduino and then the CAN bus interface

        # Create the necessary data: voleTag, rfidREADER, timestamp
        sendObj.data = str(sendObj.tagName) + "," + str(self.name) + "," + str(time.ctime())
        sendObj.send_data()
        print(sendObj.data)


class vole:
    # VOLE is a class that simply has all the info about a simulated vole
    def __init__(self, tag = None, position = None):
        self.tag = tag
        self.position = position

# Create the arduino sending object
class sender:
    # SENDER is the class object that controls the sending of data through the arduino.
    def __init__(self, tagName = 'Test', port = None, baud = 9600):
        self.port = port
        self.baudRate = baud
        self.tagName = tagName
        self.serialObj = serial.Serial(self.port, self.baudRate, timeout=1) # Set up serial object
        self.data = []
        self.startTime = None

    def send_data(self):
        # SEND_DATA does the actual sending of data through the CAN bus interface. This gets tricky because we want to control an arduino with python which isn't really possible but we can just run .ino files through the python interface so as long as we have the right ino files we're good.
        sending = self.data + "\r"
        sending = sending.encode('ascii')
        self.serialObj.write(sending)
        time.sleep(0.1)
        print(self.serialObj.readline().decode('ascii'))

    def create_data(self):
        # CREATE_DATA creates a signal to test to see if the CAN bus is sufficiently reading in the data. The vole always starts in chamber B

        self.startTime = time.time()

        # Set up all the chambers and the connections with the RFID pathways
        chamA = cageChamber(name = "A", readers = [1], chambers = ["B"])
        chamB = cageChamber(name = "B", readers = [2,3], chambers = ["A","C"])
        chamC = cageChamber(name = "C", readers = [4], chambers = ["B"])

        reader1 = rfidReader(name = 1, chamber = "A")
        reader2 = rfidReader(name = 2, chamber = "B")
        reader3 = rfidReader(name = 3, chamber = "B")
        reader4 = rfidReader(name = 4, chamber = "C")

        #self.connect_chams([chamA, chamB, chamC])
        
        # Begin the infinite loop
        testVole = vole(tag = self.tagName, position = chamB)
        while True:
            if testVole.position.name == "B": 
                # It has 3 choices, A, B, or stay
                moveChoice = np.random.randint(1,4)
                if moveChoice == 1: # A
                    # Send the reader data
                    reader2.passed(self)
                    time.sleep(np.random.rand())
                    reader1.passed(self)
                    # Change the position
                    testVole.position = chamA
                elif moveChoice == 2: # C
                    # Send the reader data
                    reader3.passed(self)
                    time.sleep(np.random.rand())
                    reader4.passed(self)
                    # Change the position
                    testVole.position = chamC
                elif moveChoice == 3: # stays
                    time.sleep(np.random.randint(2,11)) # Wait up to 10 seconds
            
            elif testVole.position.name == "A":
                # Has 2 choices, move to B or stay
                moveChoice = np.random.randint(1,3)
                if moveChoice == 1: # B
                    # Send the reader data
                    reader1.passed(self)
                    time.sleep(np.random.rand())
                    reader2.passed(self)
                    # Change the position
                    testVole.position = chamB
                elif moveChoice == 2: # stays
                    time.sleep(np.random.randint(2,11)) # Wait up to 10 seconds
            
            elif testVole.position.name == "C":
                # Has 2 choices, move to B or stay
                moveChoice = np.random.randint(1,3)
                if moveChoice == 1: # B
                    # Send the reader data
                    reader4.passed(self)
                    time.sleep(np.random.rand())
                    reader3.passed(self)
                    # Change the position
                    testVole.position = chamB
                elif moveChoice == 2: # stays
                    time.sleep(np.random.randint(2,11)) # Wait up to 10 seconds

    def reset_leds(self):
        # RESET_LEDS is the function that turns off all the leds when the script exits
        self.data = "off"
        self.send_data()

# Set up the sending object
voleSim1 = sender(tagName='vole1',port="COM4",baud=9600)
atexit.register(voleSim1.reset_leds)
time.sleep(0.1)
# Start the simulation
voleSim1.create_data() # Begins an infinite loop that creates random vole movements between 3 chambers




