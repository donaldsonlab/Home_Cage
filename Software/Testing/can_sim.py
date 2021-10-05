""" 
Date Created : 9/28/2021
Date Modified: 9/28/2021
Author: Ryan Cameron
Description: This is the collection of classes and functions that controls the simulation aspect of the home cage code. The purpose of the simulation is to be able to test functionality of the CAN bus interface by simulating the voles and having a third party interface (arduino) create CAN bus data to send to the actual hardware of the cage.
http://www.zdonaldsonlab.com/
Code located at - https://github.com/donaldsonlab/Home_Cage 
"""
# Imports
import numpy as np
import pandas as pd
import queue
import can # python-can
import serial
import time
import atexit
import threading
import logging

# Classes
"""
Some notes on the classes: Per the requirements, there need to be at least three classes, one to send information to the arduino, one to be a digital vole and have location information, and one to control the behavior of teh voles. Whether that be semi random or something much more refined and mathematically created can be changed. 
"""

class simulation_sender(threading.Thread):
    # SIMULATIONSENDER is the class, similar to the bonsai_serial_sender, that holds the necessary info to send the arduino commands to create appropriate CAN bus data. 

    def __init__(self, port = '/dev/serial0', baud = 9600, outFile = 'command_history.txt', timestamp = False):
        # Set the initial properties
        print('initializing sender')
        super().__init__()
        self.port        = port
        self.baudRate    = baud
        self.history     = queue.Queue()
        self.command_stack = queue.Queue()
        self.outFile = outFile
        self.setTime = timestamp
        self.timestamp = None
        self.timeout = 2
        # Initialize the port
        try:
            self.ser = ser.Serial(self.port, self.baudRate)
            start = time.time() 
            self.send_data('startup_test')
            
            while self.sending and time.time() - start < self.timeout:
                time.sleep(0.05)
            finished = time.time()
            if finished - start > self.timeout:
                print('serial sender failed to send test message ')
        except:
            print('Message has failed to send, stopping process.')
            # Stop the process
            exit()
        
    def finish(self):
        # FINISH is teh method that wraps everything up when the thread is exited.
        # Setup the logger
        logging.basicConfig(filename=self.outFile, format='%(levelname)s:%(message)s', level=logging.INFO)
        # Check the command history
        if not self.command_stack.empty():
            # Log all teh commands into an output file
            while not self.command_stack.empty():
                # Get the command file
                command = self.command_stack.get()
                logging.info(command)
        
    def send_data(self, message):
        # SEND_DATA is the visible level function that adds the command to the command queue to be sent.

        # Check to see if we should timestamp the data
        if self.setTime:
            # Timestamp the data
            self.timestamp = time.asctime(time.time())
            self.command_stack.put(f'{self.timestamp}:{message}')
        else:
            self.command_stack.put(message)

    def __send_data(self, message):
        # __SEND_DATA is the function that actually sends the data through the serial port
        formatted = message + '\r'
        formatted = formatted.encode('ascii')
        self.ser.write(formatted)
        print(f'MESSAGE SENT: {message}')

    def run(self):
        # RUN is the function that runs on the thread, it makes up the listener per say and listens until things are added to the command queue.

        # Endless loop
        while True:
            if self.command_stack.empty():
                # If there's nothing in the command queue
                time.sleep(0.01)
            elif not self.command_stack.empty():
                # There's a command!
                command = self.command_stack.get()
                self.__send_data(command)
                time.sleep(0.01)

class vole_behavior:
    # VOLE_BEHAVIOR is the class that controls how the simulated vole switches between chambers and how long it stays in the respective chamber.

    def __init__(self, minTime = 2, maxTime = 30):

        self.minTime = minTime
        self.maxTime = maxTime

    def choose_chamber(self, choices):
        # CHOOSE_CHAMBER chooses what chamber the vole goes into from where it currently is. This is based on a non-biased random number.

        choiceIndex = np.random.randint(len(choices))
        choice = choices[choiceIndex]




