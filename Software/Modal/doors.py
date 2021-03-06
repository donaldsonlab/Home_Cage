#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 11-01-19
# Description: This custom library contains all of the necessary python functions
#              and variables, classes, etc.. needed to control the doors in the 
#              Home Cage environment.
#####################################################################################

#from adafruit_servokit import ServoKit #UNCOMMENT FOR PI IMPLEMENTATION
from Modal.RPi import GPIO as GPIO

def openDoor(kit, val, channel):
    #################################################################################
    #Inputs: kit     - variable containing the servo controller class from ServoKit
    #        val     - Value you want the servo to move. Might get rid of this later if 
    #                  it turns out to be the same value every time.
    #        channel - Operating channel of the continuous servo
    #################################################################################
    #kit.continuous_servo[channel].throttle = val #NOTE: This is the real statement
    print("Door Opened")

def closeDoor(kit, val, channel):
    #################################################################################
    #Inputs: kit     - variable containing the servo controller class from ServoKit
    #        val     - Should be the same as the val used to open the door and the code 
    #                  just negates the same value to move the servo backwards.
    #        channel - Operating channel of the continuous servo
    #################################################################################
    #kit.continuous_servo[channel].throttle = -val #NOTE: This is the real statement
    print("Door CLosed")

    #INCLUDE THE IR LOGIC HERE