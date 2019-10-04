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
import RPi.GPIO as GPIO
import doors

#This is the variable that is the servo controller
kit = ServoKit(channels=16)

#Setup the pins for levers
GPIO.setmode(GPIO.BOARD)
