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
            self.paths = self.get_paths() # Gets possible paths chamber has to connected chambers
            self.chamberName = name # Chamber name

        def get_paths(self):
            # GET_PATHS recursively loops through the list of chambers connected to this and gets the paths it has to the connected chambers. Returns a dictionary object that has keys that are the connected chambers and values that are tuples of which RFID readers a vole needs to take to get to that chamber. Within this, the recursive aspect checks to make sure the other chamber has the connected chambers assigned correctly.

            connected = self.connChambers
            readers   = self.assocReaders
            for iCham in connected: # Loop through the chamber objects
                if isinstance(iCham,str): # If iCham is a string not an object
                    # Initialize the object
                    A = cageChamber("A",chambers = [self])
                elif isinstance(iCham,cageChamber): # It is instance of a chamber object
                    connReaders = iCham.assocReaders
                    # Look for overlaps in the connected chamber readers and the associated readers
                    np.intersect1d(list(connReaders),list(readers)) # Common readers
             

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
