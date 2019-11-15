#####################################################################################
# Donaldson Lab - 2019
# Author:      Ryan Cameron
# Date Edited: 10-31-19
# Description: This is the master script that controlls all RFID threading and doors
#              logic. This is where the RFID process and teh doors process interact
#              and exchange data.
#####################################################################################
#Set the cwd to 'Software'
import os
CWD = os.getcwd()
print(CWD)
parts = CWD.split('/')
length = len(parts)
if parts[length-1] != 'Software':
    CWD = CWD + '/Software'
    os.chdir(CWD)
    print(CWD)

import threading
import subprocess
import queue
import multiprocessing as mp 
from multiprocessing.managers import BaseManager, NamespaceProxy
from RFID import rfid_main 
from Modal import doors_main 
#####################################################################################
#NOTE: Use multiprocessing managers for the vole objects and the threading queue for 
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
#   https://www.pythonstudio.us/reference-2/managed-objects.html
#   https://www.linkedin.com/learning/python-parallel-programming-solutions/exchanging-objects-between-processes?u=42275329
#   https://stackoverflow.com/questions/26499548/accessing-an-attribute-of-a-multiprocessing-proxy-of-a-class
#####################################################################################

#Create the voleClass
class voleClass:
    def __init__(self, ping1 = None, ping2 = None, transition = None, pos = None):
        self.ping1      = ping1
        self.ping2      = ping2
        self.transition = transition
        self.pos        = pos

#Create the voleManager and Proxy
class voleManager(mp.managers.BaseManager):
    pass

class voleProxy(mp.managers.NamespaceProxy):
    _exposed_=('__getattribute__','__setattr__','__delattr__')

#Register the voleClass with the manager
voleManager.register(typeid='vole',callable=voleClass,proxytype=voleProxy)

#Now that everything is registered we can begin the script

if __name__ == "__main__":
    manager = voleManager() #Instantiate the manager
    manager.start() #Start the manager

    #####################################################################################
    #At this point the manager for communicating between the processes has been 
    #established. Each process needs to create its own proxy of the object in order to 
    #modify the properties.
    #####################################################################################

    #Need to pass the voleProxy object into both of these processes so they can communicate
    voleComm1            = manager.vole() #Instantiate the vole proxy, same attributes as voleClass
    voleComm1.transition = 0
    voleComm1.pos        = 4
    voleComm2            = manager.vole()
    voleComm2.transition = 0
    rfid_process         = mp.Process(target=rfid_main.main,  args=(voleComm1, voleComm2)) #Start the RFID tracking process
    doors_process        = mp.Process(target=doors_main.main, args=(voleComm1, voleComm2)) #Start the doors logic process

    rfid_process.start()
    #doors_process.start()

    rfid_process.join()
    #doors_process.join()