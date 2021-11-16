""" 
Date Created : 9/2/2021
Date Modified: 9/2/2021
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

# Test Script
"""
This section is for running test scripts for the code. If you want to run this test you must run this script as the main script. It will not be run if called from another file. 
"""

if __name__ == "__main__": # If this is the main script
    # Setup commands to send
    voleTag = 1256
    timestamp = time.time()
    rfidNum = 4
    data = bytearray([voleTag, rfidNum], encoding='hex')

    # Setup the Bus
    bus = can.Bus(channel='can0') # /dev port on the pi where the can bus is connected to I think

    # Send the command to the arduino
    msg = can.Message(timestamp=timestamp,data=data)
    bus.send(msg=msg)

    # Recieve confirmation from the Arduino

