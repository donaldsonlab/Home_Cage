#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 10-3-19
# Description: This file is a setup file for the raspberry pi to import and install
#              all the necessary python packages and change the settings accordingly.
#####################################################################################

import os
import subprocess
import sys

def getPackage(name):
    if name in installed_packages:
        print(name + " is already installed")
    else:
        command = "pip3 install " + name
        os.system(command)
        print(name + " installed")

if __name__ == "__main__":
    #Get list of installed packages
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    #Print out versions of necessary packages
    os.system("python --version")
    os.system("pip3 --version")

    #Start checking for necessary packages
    getPackage("RPI.GPIO")
    getPackage("adafruit-blinka")
    getPackage("adafruit-circuitpython-servokit")
    getPackage("threading")
    getPackage("pyserial")
    getPackage("queue")

    #########################################################
    #This is where I have no idea if these things are going
    #to work or not
    #########################################################
    #Configure I2C and SPI settings

    functionCall = subprocess.call(["sudo","i2cdetect","-y","1"])
    if functionCall == 0:
        print("I2C Enabled")
    else:
        print("I2C Disabled\n")
        print("Enabling...")

        #Begin enabling I2C

        #####################################################
        #Here we need to edit the text file:/etc/modprobe.d/raspi-blacklist.conf
        #Go to: http://ozzmaker.com/i2c/ for full instructions
        #on how to programmatically enable I2C.
        #####################################################

    #########################################################
    #Repeat the same I2C editing process for enabling the SPI
    #functionality on the Pi
    #########################################################