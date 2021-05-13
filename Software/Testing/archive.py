def move(self,moveChance = 50):
        # MOVE is the function that loops through until the stop time of the simulation is met in order to create random movements of the vole throughout the chamber. This drives the creation of the data sent through the CAN bus interface.
        # The "chamber" is organized so that the RFID readers are aligned like:
        # |---------------------------|
        # |           B               |
        # |---------------------------|
        #     |2|             |3|  
        #     | |             | |
        #     |1|             |4|  
        # |---------------------------|
        # |           A               |
        # |---------------------------| 

        # Determine its options based on where it starts
        startTime = time.time() # Seconds since the latest epoch in local time
        loc = self.startLoc # Set the first location
        while True: # Begin the simulation
            # Makes decision based on starting location
            if loc == "A":
                currentTime = time.time()
                random.seed(currentTime)
                decision = random.randint(0,1)
                if decision == 0: # Right tunnel
                    loc = "C"
                    random.seed(time.time())
                    decision2 = random.randint(0,1)
                    if decision2 == 0: # Continue forward
                        loc = "B"
                    elif decision2 == 1: # Turn Back
                        loc = "A"
                elif decision == 1: # Left tunnel
                    loc = "D"
                    random.seed(time.time())
                    decision2 = random.randint(0,1)
                    if decision2 == 0: # Continue forward
                        loc = "B"
                    elif decision2 == 1: # Turn Back
                        loc = "A"
                    
            elif loc == "B":
                currentTime = time.time()
                random.seed(currentTime)
                decision = random.randint(0,1)
                if decision == 0: # Right tunnel
                    loc = "C"
                    random.seed(time.time())
                    decision2 = random.randint(0,1)
                    if decision2 == 0: # Continue forward
                        loc = "A"
                    elif decision2 == 1: # Turn Back
                        loc = "B"
                elif decision == 1: # Left tunnel
                    loc = "D"
                    random.seed(time.time())
                    decision2 = random.randint(0,1)
                    if decision2 == 0: # Continue forward
                        loc = "A"
                    elif decision2 == 1: # Turn Back
                        loc = "B"
            # END IF

        # END WHILE