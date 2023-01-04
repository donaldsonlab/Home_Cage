'''
Needs Testing. 

Not an experiment script, just writing a function so I can see pin values. 
'''
import time 
import RPi.GPIO as GPIO
from tabulate import tabulate

import os, sys
cwd = os.getcwd()
sys.path.append(cwd)
# sys.path.append(os.path.join(os.path.dirname(__file__), "Map"))
from Control.Classes.Map import Map 

GPIO.setmode(GPIO.BCM)

map_to_test = Map(cwd + '/Control/Configurations', 'map_operant.json') # optional argument: map_file_name to specify filepath to a different map configuration file 

def main(map):

    interactable_with_pin = []
    for (name, interactable) in map.instantiated_interactables.items(): 
        if hasattr(interactable, 'buttonObj'): 
            interactable.buttonObj
            interactable_with_pin.append(interactable)
    

    # Extend Levers 
    for i in interactable_with_pin: 
        if i.type == 'lever': 
            i.extend()


    # Check value with method
    while(True):

        try: 

            status = []

            for i in interactable_with_pin: 

                channel = i.buttonObj.pin_num

                print("\033c", end="")
                
                threshold_attr_name = i.threshold_condition["attribute"]
                attribute = getattr(i, threshold_attr_name) # get object specified by the attribute name                
                # check for attributes that may have been added dynamically 
                if hasattr(i, 'check_threshold_with_fn'): # the attribute check_threshold_with_fn is pointing to a function that we need to execute 
                    attribute = i.check_threshold_with_fn(i) # sets attribute value to reflect the value returned from the function call

                status += [[i.name, channel, GPIO.input(channel)]] # pressed_val == 0 

            print(tabulate(status, headers = ['interactable', 'pin', 'status']))
            time.sleep(0.05)



        except KeyboardInterrupt:
            print('\n bye!')
            exit()


    while(True):

        try: 
            status = []
            for channel in range(0,20): 
                print("\033c", end="")
                status += [[channel, GPIO.input(channel)]] # pressed_val == 0 
            print(tabulate(status, headers = ['pin', 'status']))
            time.sleep(0.05)

        except KeyboardInterrupt:
            map.deactivate_interactables()
            print('\n bye!')
            exit()



main(map_to_test)