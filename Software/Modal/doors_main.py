#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 10-4-19
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
#MODE 1
#####################################################################################

#Depending on the intitial position of the vole, wait for the lever. 
if initialPos == 1:
    GPIO.wait_for_edge(leverPin1, GPIO_RISING)
elif initialPos == 2:
    GPIO.wait_for_edge(leverPin2, GPIO_RISING)

#Now do the door logic
doors.openDoor(kit, .7, 0)

#Wait for RFID Tag that we passed
######################################################################################
#MODE 2
#####################################################################################

#Loop that waits for RFID tag to pass.
#IF passed     -> move to MODE 3
#IF not passed -> wait for animal to pass, update RFID pings
#    IF time passed -> close door, move back to MODE 1

while True:
    #Find most recent positions of the animals
    posTag1 = rfid.findTag("vole_1")
    posTag2 = rfid.findTag("vole_2")
    pos1 = int(posTag1[1])
    pos2 = int(posTag2[1])
    

#####################################################################################
#MODE 3
#####################################################################################

#Just continuously update RFID marks
#IF animal in same cage -> continue update
#IF animals separate -> move back to MODE 2