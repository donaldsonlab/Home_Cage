"""
Authors: Ryan Cameron
Date Created: 6/20/2023
Date Modified: 6/20/2023
Description: This class is the Pico-side implementation of the gpio expansion for operant-type interactables. The Pi side code is added as functionality in the interactableABC class. 

Property of Donaldson Lab at the University of Colorado at Boulder
"""

class Signal:
    def __init__(self):
        """
        Need to set up communications channels to the raspberry pi. This is done through a web server hosted on the pico. 
        """
