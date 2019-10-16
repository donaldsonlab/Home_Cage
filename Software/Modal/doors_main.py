#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 10-11-19
# Description: This is the main script for controlling the doors. All of the modal 
#              logic (Mode 1,2,3) changes and control is here. This includes the 
#              door logic, IR logic, and RFID pulling. This will most likely turn 
#              out to be the main script for the Home Cage environment.
#####################################################################################

from adafruit_servokit import ServoKit
from Software.Modal.RPi import GPIO as GPIO
from Software.Modal import doors
from Software.Modal import rfidLib as rfid
from Software.RFID.rfid_main import vole
import time
import threading
import queue

def mode1(initialPos):
    #####################################################################################
    #MODE 1
    #####################################################################################
    
    #Depending on the intitial position of the vole, wait for the lever. 
    if initialPos == 1:
        GPIO.wait_for_edge(leverPin1, GPIO_RISING)
    elif initialPos == 2:
        GPIO.wait_for_edge(leverPin2, GPIO_RISING)

    #Now do the door logic
    doors.openDoor(kit, .7, 0)
    thread_mode2.start()

def mode2():
    ######################################################################################
    #MODE 2
    #####################################################################################

    #Loop that waits for RFID tag to pass.
    #IF passed     -> move to MODE 3
    #IF not passed -> wait for animal to pass, update RFID pings
    #    IF time passed -> close door, move back to MODE 1

    timeout = 15 #Amount of time for the door to remain open
    startTime = time.time() #Gets the time in seconds
    while True:
        newTime = time.time()
        elapsedTime = newTime - startTime
        if elapsedTime > timeout:
            thread_mode1.start()
            break #Move back to mode 1

        #Find most recent positions of the animals
        vole1 = rfid.findPos(1) #Test animal
        vole2 = rfid.findPos(2) #Partner Animal

        #REMEMBER - at the beginning, the animals are in separate cages
        if vole1.pos == vole2.pos:
            thread_mode3.start()
            break #move on to mode 3

def mode3():
    #####################################################################################
    #MODE 3
    #####################################################################################

    #Just continuously update RFID marks
    #IF animal in same cage -> continue update
    #IF animals separate -> move back to MODE 2
    #Track the position variable in the vole class

    while True:
        vole1 = rfid.getVole(1)
        if vole1.transition == 1:
            thread_mode2.start()
            break #go to mode 2
        #Also track animal 2 if necessary, don't know if it is though

if __name__ == "__main__":
    #####################################################################################
    #Setup
    #####################################################################################
    leverPin1 = 17
    leverPin2 = 18

    #This is the variable that is the servo controller
    kit = ServoKit(channels=16)

    #Setup the pins for levers
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(leverPin1, GPIO.IN) #Sets up channel 17 as the lever channel
    GPIO.setup(leverPin2, GPIO.IN)

    #Now find which cage the animal is first in
    RFID_initialTag = rfid.get()
    if "vole_1" in RFID_initialTag[0]:
        initialPos = int(RFID_initialTag[1]) #Initial cage number of the vole
    else:
        RFID_initialTag = rfid.findTag("vole_1")
        initialPos = int(RFID_initialTag[1])

    #Optional Manual initial Position
    #initialPos = 1

    #####################################################################################
    #Start the threading
    #####################################################################################
    thread_mode1 = threading.Thread(target=mode1) #Start mode 1 thread
    thread_mode2 = threading.Thread(target=mode2)
    thread_mode3 = threading.Thread(target=mode3)

    thread_mode1.start()

    #####################################################################################
    #This should now be running on an infinite loop as each mode always either points 
    #to another mode or keeps running infinitely itself. Need some sort of ext condition.
    #Maybe this is where we need to include some sort of command interface that connects
    #the user to the process.
    #####################################################################################