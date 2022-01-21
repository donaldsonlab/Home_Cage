""" 
Date Created : 10/5/2021
Date Modified: 10/5/2021
Author: Ryan Cameron
Description: This script tests the pipeline of sending and recieving CAN bus messages through the PC -> Arduino -> Raspberry PI
Property of Donaldson Lab, University of Colorado Boulder, PI Zoe Donaldson
http://www.zdonaldsonlab.com/
Code located at - https://github.com/donaldsonlab/Home_Cage 
"""
# Imports
import numpy as np 
import serial
import time
import can
from read_can import message 

# Classes

# Test Script
if __name__ == "__main__":
    # Send the data
    messObj = message(isserial=False)

    # Create listener for the message
    messObj.listen()

    # Send the message
    # print("Sleeping...")
    # time.sleep(1)
    # print("Awake")
    # messObj.self_send(data = bytearray([1,2,3,4]))

    # print("Recieving...")
    # time.sleep(2)

    # Infinite loop to listen
    while True:
        time.sleep(0.5)


