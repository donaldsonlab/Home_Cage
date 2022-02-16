""" 
This is an example scenario as well, implementing the scenario where there are two animals in the Home Cage setup and they are free to move around as long as the correct conditions have been met. The modes are outlined below. 
"""

# Imports
import time
from Modal import mode as md

# Set up the Map
exampleBox = Map("exampleConfig.json")
chamber_lever = md.lever()
door_1 = md.door()
rfid_1 = md.rfid()
rfid_2 = md.rfid()


# Mode Classes
class modeOpen(md.modeABC):
    """This mode represents the "open" mode where the test animal and the tethered animal have free access to one another. The door is open here and requires no operant task to complete.
    """

    def __init__(self, map=None, timeout=None):
        # Init the parent
        super().__init__(map, timeout)

    def enter(self):
        # Set the default states
        self.box.chamber_lever.retract()
        self.box.door_1.default = True
        self.box.door_1.trigger = None

        pass

    def run(self):
        pass

    def exit(self):
        pass

class modeOperant(md.modeABC):
    """This mode requires an operant task to be performed for the vole to move into the other chamber and see the tethered animal. 
    """

    def __init__(self, map=None, timeout=None):
        # Init the super
        super().__init__(map, timeout)

    def enter(self):
        # Set the default states
        self.box.chamber_lever.extend()
        self.box.door_1.default = False
        self.box.door_1.trigger = chamber_lever

    def run(self):

        # Increase the number of presses when the lever is pressed
        while ((time.now - self.startTime) < self.timeout):

            # Increase the number of presses if the lever has been pressed
            if self.box.chamber_lever.threshold:
                self.box.chamber_lever.numPresses += 1
        
        # Run the exit function after the timeout
        self.exit()

    def exit(self):
        pass

class modeIdle(md.modeABC):
    """This mode is the so called "idle" mode where the system does not have any operant tasks readied and the doors are all close, with the animals separated. The only way to exit this mode is either by timeout or an interrupt call directly by the user. 
    """

    def __init__(self, map=None, timeout=None):
        # Init the super
        super().__init__(map, timeout)

    def enter(self):
        # Set the default states
        self.box.chamber_lever.retract()
        self.box.door_1.trigger = None
        self.box.door_1.default = True

    def run(self):

        # Until timeout simply wait
        while ((time.now - self.startTime) < self.timeout):
            pass

        # Exit the mode
        self.exit()

    def exit(self):
        pass

# Run the stuff
if __name__ == "__main__":

    # Instantiate the modes
    mdOperant = modeOperant(timeout=21600)
    mdIdle    = modeIdle(timeout=54000)
    mdOpen    = modeOpen(timeout=10800)