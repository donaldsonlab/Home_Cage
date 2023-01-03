'''
Needs Testing. 

Not an experiment script, just writing a function so I can see pin values. 
'''
import time 
import RPi.GPIO as GPIO
from tabulate import tabulate


# Check value with method
while(True):

    try: 
        status = []
        for channel in range(0,20): 
            print("\033c", end="")
            status += [[channel, GPIO.input(channel)]] # pressed_val == 0 
        print(tabulate(status, headers = ['pin', 'status']))
        time.sleep(0.05)

    except KeyboardInterrupt:
        print('\n bye!')
        exit()