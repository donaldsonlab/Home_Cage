# This script is testing the basic functionality of controlling an arduino board with python. It uses the pyfirmata library in conjunction with the firmataStandard sketch uploaded to the Arduino board to communicate. Details and references are found through this link: https://hub.packtpub.com/prototyping-arduino-projects-using-python/, https://realpython.com/arduino-python/#hello-world-with-arduino-and-python

# Imports
import pyfirmata as pf
import numpy as np
import time
import random

# Setup the arduino board
port = 'COM4'
board = pf.Arduino(port) # Sets up the arduino board object that can be acted upon

def blink(board, maxBlinks=None):
    # Simple blink script to test that the blink is working

    count = 1
    while True:
        board.digital[13].write(1)
        time.sleep(1)
        board.digital[13].write(0)
        time.sleep(1)
        if maxBlinks != None:
            count = count + 1
            if count >= maxBlinks:
                break

class voleSim:
    # VOLESIM is a simulation object for the test. This contains all the functions and properties necessary to start, run, and end a simultion with the necessary data output into a CAN Bus format and sent to a Raspberry Pi.
    class cageChamber:
        def __init__(self,name,reader = [None], chambers = [None]):
            self.assocReaders = reader # RFID Readers connected to the chamber
            self.connChambers = chambers # Chamber objects connected to this one
            self.chamberName = name # Chamber name
            self.readers() # Connect reader objects to this chamber
            self.connect() # Connect to the other chambers
            #self.paths = self.connect() # Gets possible paths chamber has to connected chambers

        def connect(self):
            # GET_PATHS recursively loops through the list of chambers connected to this and gets the paths it has to the connected chambers. Returns a dictionary object that has keys that are the connected chambers and values that are tuples of which RFID readers a vole needs to take to get to that chamber. Within this, the recursive aspect checks to make sure the other chamber has the connected chambers assigned correctly.

            connected = self.connChambers
            newConnected = []
            for iCham in connected: # Loop through the chamber objects
                if isinstance(iCham,str): # If iCham is a string not an object
                    # Initialize the object
                    relatedCham = voleSim.cageChamber(iCham,chambers = [self])
                    newConnected = newConnected + [relatedCham] # Adds chamber object to connected
                elif isinstance(iCham,voleSim.cageChamber): # It is instance of a chamber object
                    # Add any extra connected chambers
                    newConnected = newConnected + [iCham]
                    # Look for overlaps in the connected chamber readers and the associated readers
            self.connChambers = newConnected # Sets the assigned connected chambers
        
        def readers(self):
            # READERS creates the RFID reader objects and connects them to the chamber they are associated with.
            readers = self.assocReaders
            newReaders = []
            for iRead in readers: # Loop through the RFID numbers
                if isinstance(iRead,int):
                    # Create the object and associate it
                    readerObj = voleSim.cageReader(iRead,chamber=self)
                    newReaders = newReaders + [readerObj]
                elif isinstance(iRead, voleSim.cageReader):
                    # If already an object make sure its connected correcly
                    iRead.connChamber = self
                    newReaders = newReaders + [self]
            self.assocReaders = newReaders

        def get_paths(self):
            # GET_PATHS gets the paths a vole has to travel to get from one chamber to another
            blah = 1
    
    class cageReader:
        # CAGEREADER is the base class for an rfid reader in the system
        def __init__(self,name,chamber=None):
            self.readerName = name
            self.connChamber = chamber # Chamber this reader is connected to
            self.connect() # Connect the reader to a chamber object

        def connect(self):
            # CONNECT connects the reader object to a chamber object
            connected = self.connChamber
            for iCham in [connected]:
                if isinstance(iCham,str): # Create the chamber object
                    newChamber = voleSim.cageChamber(iCham,reader=[self])
                elif isinstance(iCham,voleSim.cageChamber): # Already a valid object
                    newChamber = iCham
                connReaders = newChamber.assocReaders
                inds = np.where(np.array(connReaders) == self.readerName)
                inds = inds[0][0]
                newChamber.assocReaders[inds] = self # Change from number to reader object
            self.connChamber = newChamber
             

    def __init__(self,voleTag = "simuVole", stopTime = 300, startLoc = "A"):
        self.voleTag  = voleTag
        self.stopTime = stopTime
        self.startLoc = startLoc

    def move(self,moveChance = 50):
        # MOVE is the function that loops through until the stop time of the simulation is met in order to create random movements of the vole throughout the chamber. This drives the creation of the data sent through the CAN bus interface.
        # The "chamber" is organized so that the RFID readers are aligned like:
        # |-------------------------|
        # |           B             |
        # |-------------------------|
        #     |2|             |3|  
        #     | |             | |
        #     |1|             |4|  
        # |---------|     |---------|
        # |    A    |     |    C    |
        # |---------|     |---------| 

        return None
####################################################################################################
# Now setup testing for the COM interface
# Create the sim object
sim = voleSim

# Create all the chamber objects
aCham = sim.cageChamber("A",reader = [1],chambers=["B"])
bCham = sim.cageChamber("B",reader=[2,3],chambers=[aCham,"C"])
cCham = sim.cageChamber("C",reader=[4],chambers=[bCham])


blah = 1