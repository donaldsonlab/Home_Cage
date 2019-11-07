#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 10-31-19
# Description: This is a library of all the functions needed to control the shared
#              memory with the RFID thread (operating on a separate core). This
#              library is imported into the main script so that it can communicate
#              with the other process.
#####################################################################################

import threading
import queue
import subprocess
from RFID.rfid_main import voleClass

def getVole(voleNum):
    #Inputs  - voleNum: number of the vole queue to pull from (1=test)
    #Outputs - vole#: vole proxy object of the necessary vole
    #This function just pulls the rfid tag from shared memory
    if voleNum == 1: #Test
        vole1 = voleClass()
        return vole1
    elif voleNum == 2: #Partner
        vole2 = voleClass()
        return vole2
    

def findPos(voleComm):
    #Inputs  - voleNum: number of the vole queue to pull from (1=test)
    #Outputs - voleObject: vole object of the requested vole containing position information
    #This function finds the most recent appearance of 'name' in the shared memory queue
    if voleComm.ping2 == 3:
        voleComm.pos = 2
    elif (voleComm.ping2 == 1) | (voleComm.ping2 == -1):
        voleComm.pos = 0
    elif voleComm.ping2 == -3:
        voleComm.pos == -2
    else:
        print("Problem Reading RFID Tag") #If the position is 'None' for instance
    
    return voleComm