#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 10-11-19
# Description: This is the master script that controlls all RFID threading and doors
#              logic. This is where the RFID process and teh doors process interact
#              and exchange data.
#####################################################################################

import threading
import subprocess
import queue
import multiprocessing as mp 
#####################################################################################
#NOTE: Use multiprocessing queues for the vole objects and the threading queue for 
#      the list object of all the RFID pings.
#####################################################################################

#####################################################################################
#NOTES ON HOW TO DO SHARED MEMORY BETWEEN PROCESSES
#Use Mangers in the multiprocess library:
#   https://docs.python.org/3/library/multiprocessing.html#managers
#   This stores some object in shared memory. To access the shared memory object,
#       other process must use proxies.
#       https://docs.python.org/3/library/multiprocessing.html#proxy-objects
#       This is most likely the best way to go. 

#Helpful Links:
#   https://stackoverflow.com/questions/3671666/sharing-a-complex-object-between-python-processes
#####################################################################################

