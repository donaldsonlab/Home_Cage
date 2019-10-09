#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 10-4-19
# Description: This is a library of all the functions needed to control the shared
#              memory with the RFID thread (operating on a separate core). This
#              library is imported into the main script so that it can communicate
#              with the other process.
#####################################################################################

import threading
import queue
import subprocess

def get():
    #This function just pulls the rfid tag from shared memory
    RFID_tag = ["vole1","1"] #Just an example so there's something here
    return RFID_tag

def findTag(name):
    #This function finds the most recent appearance of 'name' in the shared memory queue
    RFID_tag = [name,"1"]
    return RFID_tag