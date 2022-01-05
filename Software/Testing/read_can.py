""" 
Date Created : 9/2/2021
Date Modified: 11/18/2021
Author: Ryan Cameron
Description: is the file that contains all of the necessary classes and functions to read data coming in through a CAN-bus line on the raspberry pi and send/store it for reference.
Property of Donaldson Lab, University of Colorado Boulder, PI Zoe Donaldson
http://www.zdonaldsonlab.com/
Code located at - https://github.com/donaldsonlab/Home_Cage 
"""

# Imports
import can 
import serial
import time

# Classes
class message:
    """MESSAGE class is what contains the message data, string conversion, timestamp, and all relevant info and functions to recieve, read, and log the message.
    """
    def __init__(self, isserial = False):
        self.timestamp = None
        self.command = None

        # Check if its a serial bus
        if isserial:
            self.bus = can.interfaces.serial.serial_can.SerialBus(channel = "/dev/tty0")
        else:
            self.bus = can.interface.Bus() # Should auto configure the bus, make sure that this is interface.Bus NOT can.Bus

        pass

    # This function recieves the message through the CAN bus shield
    def recieve(self):
        """This function recieves the message and parses up the object to properties in the native object here. 
        """
        recMessage = self.bus.recv()
        print("Message Recieved")
        self.byteData = recMessage.data
        self.command = self.byteData.hex()
        print("Recieved Command: " + self.command)

    def self_send(self, data):
        """This function send the specified data in bytearray form to a serial port on the Pi

        Args:
            data (bytearray): Maximum of 8 bytes, data to send over CAN
        """

        # Check length of bytearray
        if len(data) > 8:
            raise ValueError("Must be 8 bytes or shorter")
        
        # Send the message
        self.bus.send(msg = can.Message(data = data), timeout = 3)

# Test Script
"""
This section is for running test scripts for the code. If you want to run this test you must run this script as the main script. It will not be run if called from another file. This test specifically is meant to test the functionality of reading CAN bus data that is being sent to it over the pi hat.
"""

if __name__ == "__main__": # If this is the main script
    # Setup the BUS to recieve CAN message from arduino
    testMess = message()

    # Recieve the data
    testMess.recieve()

