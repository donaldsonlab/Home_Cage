#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 11-01-19
# Description: This is the main script for controlling the doors. All of the modal 
#              logic (Mode 1,2,3) changes and control is here. This includes the 
#              door logic, IR logic, and RFID pulling. This will most likely turn 
#              out to be the main script for the Home Cage environment.
#####################################################################################

#from adafruit_servokit import ServoKit #UNCOMMENT FOR PI IMPLEMENTATION
from Modal.RPi import GPIO as GPIO
from Modal import doors
from Modal import rfidLib as rfid
from RFID.rfid_main import voleClass
import time
import threading
import queue
from Modal.threadVars import threadClass

def mode1(initialPos,servoDict,modeThreads):
    #####################################################################################
    #MODE 1
    #####################################################################################

    leverPin1 = servoDict.get("leverPin1")
    leverPin2 = servoDict.get("leverPin2")
    kit = servoDict.get("kit")
    #Depending on the intitial position of the vole, wait for the lever. 
    if initialPos == 1:
        GPIO.wait_for_edge(leverPin1, GPIO_RISING)
    elif initialPos == 2:
        GPIO.wait_for_edge(leverPin2, GPIO_RISING)
    else:
        print("ANIMAL IN INVALID STARTING CAGE. ENSURE ANIMALS ARE SEPARATED")
        #Whatever shutdown conditions are needed
        #return

    #Now do the door logic
    doors.openDoor(kit, .7, 0)
    modeThreads.refresh2(target = mode2, args = (modeThreads,))
    modeThreads.thread_mode2.start()

def mode2(modeThreads):
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
            modeThreads.refresh1(target = mode1, args = (modeThreads.initialPos, modeThreads.servoDict, modeThreads))
            modeThreads.thread_mode1.start()
            break #Move back to mode 1

        #Find most recent positions of the animals
        vole1 = rfid.findPos(1) #Test animal
        vole2 = rfid.findPos(2) #Partner Animal

        #REMEMBER - at the beginning, the animals are in separate cages
        if vole1.pos == vole2.pos:
            modeThreads.refresh3(target = mode3, args = (modeThreads,))
            modeThreads.thread_mode3.start()
            break #move on to mode 3

def mode3(modeThreads):
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
            modeThreads.refresh2(target = mode2, args = (modeThreads,))
            modeThreads.thread_mode2.start()
            break #go to mode 2
        #Also track animal 2 if necessary, don't know if it is though

def main():
    #if __name__ == "__main__":
    #####################################################################################
    #Setup
    #####################################################################################
    leverPin1 = 17
    leverPin2 = 18

    #This is the variable that is the servo controller
    #kit = ServoKit(channels=16) #UNCOMMENT FOR PI IMPLEMENTATION
    kit = None #COMMENT FOR PI IMPLEMENTATION
    servoDict = {
        "leverPin1": leverPin1,
        "leverPin2": leverPin2,
        "kit"      : kit,
    }
    #Setup the pins for levers
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(leverPin1, GPIO.IN) #Sets up channel 17 as the lever channel
    GPIO.setup(leverPin2, GPIO.IN)

    #Now find which cage the animal is first in
    RFID_initialTag = rfid.getVole(1)
    initialPos = RFID_initialTag.pos
    #if "vole_1" in RFID_initialTag[0]:
        #initialPos = int(RFID_initialTag[1]) #Initial cage number of the vole
    #else:
        #RFID_initialTag = rfid.findTag(1)
        #initialPos = int(RFID_initialTag[1])

    #Optional Manual initial Position
    #initialPos = 1
    initialPos = 18 #FOR TESTING PURPOSES
    #####################################################################################
    #Start the threading
    #####################################################################################
    #instantiate a threadClass object
    modeThreads = threadClass(thread_mode1 = threading.Thread(), thread_mode2 = threading.Thread(), thread_mode3 = threading.Thread(), initialPos = initialPos, servoDict = servoDict)

    #Define the thread parameters
    modeThreads.thread_mode1._target = mode1
    modeThreads.thread_mode1._args = tuple([initialPos,servoDict,modeThreads])

    modeThreads.thread_mode2._target = mode2
    modeThreads.thread_mode2._args = tuple([modeThreads])

    modeThreads.thread_mode3._target = mode3
    modeThreads.thread_mode3._args = tuple([modeThreads])

    #target1 = list(threadClass.thread_mode1._args)
    #target1[0] = mode1
    modeThreads.thread_mode1.start()

        #####################################################################################
        #This should now be running on an infinite loop as each mode always either points 
        #to another mode or keeps running infinitely itself. Need some sort of ext condition.
        #Maybe this is where we need to include some sort of command interface that connects
        #the user to the process.
        #####################################################################################