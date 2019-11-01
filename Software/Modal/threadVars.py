#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 11-01-19
# Description: This is a script that contains the variables for each mode(1,2,3) 
#              thread that exists. 
#####################################################################################
import threading 

class threadClass():
    def __init__(self, thread_mode1 = threading.Thread(), thread_mode2 = threading.Thread, thread_mode3 = threading.Thread(), initialPos = None, servoDict = None):
        self.thread_mode1 = thread_mode1
        self.thread_mode2 = thread_mode2
        self.thread_mode3 = thread_mode3
        self.initialPos   = initialPos
        self.servoDict    = servoDict

    def refresh1(self, target, args):
        self.thread_mode1 = threading.Thread(target=target, args= args)

    def refresh2(self, target, args):
        self.thread_mode2 = threading.Thread(target=target, args= args)

    def refresh3(self, target, args):
        self.thread_mode3 = threading.Thread(target=target, args= args)
