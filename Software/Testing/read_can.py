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
from can.interfaces.serial.serial_can import *
import threading
import os

# Classes
class message:
    """MESSAGE class is what contains the message data, string conversion, timestamp, and all relevant info and functions to recieve, read, and log the message.
    """
    def __init__(self, isserial = False):
        # Initialize the canBUS 
        print("Initializing can bus")
        try:
            os.system('sudo /sbin/ip link set can0 up type can bitrate 500000')
            print("CAN init ok")
        except:
            raise OSError("CAN init FAILED")

        # Start object initialization
        print("Initializing...")
        self.timestamp = None
        self.command = None

        # Check if its a serial bus
        if isserial:
            print("Seting up serial bus...")
            self.bus = SerialBus(channel = "/dev/tty1")
            print("Serial bus created")
        else:
            print("Setting up CAN bus...")
            self.bus = can.interface.Bus(channel = "can0", bustype='socketcan_native') # Should auto configure the bus, make sure that this is interface.Bus NOT can.Bus
            print("Bus created")
        
        print("Message object created")

    # This function recieves the message through the CAN bus shield
    def recieve(self):
        """This function recieves the message and parses up the object to properties in the native object here. 
        """

        print("Attempting to recieve...")
        recMessage = self.bus.recv(timeout = 3)
        print("Message Recieved")
        print(recMessage)

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
        print("Sending...")
        self.bus.send(msg = can.Message(data = data), timeout = 3)
        print("Data sent")

    def listen(self):
        """This function creates a listener on its own thread and listens for messages sent over the serial connection, it uses the can Notifier base class to listen. 
        """

        # Create notifier
        notiThread = threading.Thread(target=self.__listen)
        notiThread.start()

    def __listen(self):
        """Internal method for the listen method to call that actually has all the functionality and can be threaded.
        """

        print("Listening...")
        noti = can.Notifier(bus=self.bus,listeners=[can.Printer()], timeout = 5)

    def sendCAN(self, data, repeat=False):
        

        

# Test Script
"""
This section is for running test scripts for the code. If you want to run this test you must run this script as the main script. It will not be run if called from another file. This test specifically is meant to test the functionality of reading CAN bus data that is being sent to it over the pi hat.

Note: To set up the pi and initialize the 
"""

if __name__ == "__main__": # If this is the main script
    # Setup the BUS to recieve CAN message from arduino
    testMess = message(isserial = True)

    # Send the data
    toSend = bytearray([1,3,5,7])
    testMess.self_send(toSend)
    time.sleep(2)

    # Recieve the data
    testMess.recieve()

