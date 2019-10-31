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
    #Outputs - vole#: vole object of the necessary vole
    #This function just pulls the rfid tag from shared memory
    if voleNum == 1: #Test
        vole1 = voleClass()
        return vole1
    elif voleNum == 2: #Partner
        vole2 = voleClass()
        return vole2
    

def findPos(voleNum):
    #Inputs  - voleNum: number of the vole queue to pull from (1=test)
    #Outputs - voleObject: vole object of the requested vole containing position information
    #This function finds the most recent appearance of 'name' in the shared memory queue
    voleObject = getVole(voleNum)
    if voleObject.ping2 == 3:
        voleObject.pos = 2
    elif abs(voleObject.ping2) == 1:
        voleObject.pos = 0
    elif voleObject.ping2 == -3:
        voleObject.pos == -2
    else:
        print("Problem Reading RFID Tag")
    
    return voleObject