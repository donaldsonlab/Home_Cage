""" 
Date Created : 8/13/2021
Date Modified: 8/13/2021
Author: Ryan Cameron
Description: file that contains all of the necessary classes and functions to read data coming in through a CAN-bus line on the raspberry pi and send/store it for reference.
Property of Donaldson Lab, University of Colorado Boulder, PI Zoe Donaldson
http://www.zdonaldsonlab.com/
Code located at - https://github.com/donaldsonlab/Operant-Cage 
"""
# Imports
import can # python-can

# Reader object
class reader:
    # READER is the object that reads the in the CAN bus info
    def __init__(self, name = None):
        self.name = name

# Sender
class sender:
    # SENDER is the object in charge of sending the information over the canbus connection
    def __init__(self, name = None, message = None):
        self.name = name
        self.bus = can.interface.bus()
        self.message = message

    def send_msg(self):
        # SEND_MSG sends the message stored in the message property
        

