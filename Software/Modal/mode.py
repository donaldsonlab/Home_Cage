"""
Authors: Ryan Cameron
Date Created: 1/24/2022
Date Modified: 1/24/2022
Description: This is the class file for the mode classes which contain all the information for the control software of the Homecage project to move between different logic flows. Each mode of operation has a different flow of logic, and this file contains the base class and any extra classes that are necessary to manage that.

Property of Donaldson Lab at the University of Colorado at Boulder
"""

# Classes
class mode:
    """This is the base class, each mode will be an obstantiation of this class.
    """

    def __init__(self):
        self.rfidQ = None
        self.box = None
        self.threads = None
        pass

    def threader(self):
        """This is a decorator function that will be added to any method here that needs to run on its own thread. It simply creates, starts, and logs a method to a thread. 
        """
        pass

    def enter(self):
        """This method runs when the mode is entered from another mode. Essentially it is the startup method. This differs from the __init__ method because it should not run when the object is created, rather it should run every time this mode of operation is started. 
        """
        pass

    @threader
    def listen(self):
        """This method listens to the rfid queue and waits until something is added there.
        """
        pass

    def run(self):
        """This is the main method that contains the logic for the specific mode. It should be overwritten for each specific mode class that inherits this one. Because of that, if this function is not overwritten it will raise an error on its default. 
        """

        # If not overwritten, this function will throw the following error
        raise NameError("This function must be overwritten with specific mode logic")

    @threader
    def exit(self):
        """This function is run when the mode exits and another mode begins. It closes down all the necessary threads and makes sure the next mode is setup and ready to go. 
        """
        pass