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
from Software.Testing.can_sim import simulation_sender

# Classes

# Test Script
if __name__ == "__main__":
    # Send the arduino a signal to create data
    sender = simulation_sender(port = "COM4", timestamp = True)

    # Create the data
    voleTag = "1244"
    rfidNum = 2
    message = f'{voleTag}:{rfidNum}' # Everything is delimited by a : symbol

    # Give the arduino the data
    sender.send_data(message) # Will timestamp the data
    
    #