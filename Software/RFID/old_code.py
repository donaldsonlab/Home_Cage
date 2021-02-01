def rfidTrack_1(eventDict,voleDict):
    #Defines the serial port and the binary data stream characteristics
    serial_1 = serial.Serial(
        port = '/dev/ttySC0', #serial0 for Pi port
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    # Set the tracker variables
    tracker1 = tracker()
    tracker1.set_variables(eventDict, voleDict)

    while True:
        #Set the event value to false
        tracker1.event1.clear()
        #print("start1\n")
        line_1 = serial_1.readline()
        if tracker1.voleTag1 in line_1.decode():
            print('Vole 1 Ping 1')
            if tracker1.voleComm1.transition == 0: #Entering transition
                tracker1.voleComm1.ping1 = 1 #RFID number of the ping
                tracker1.voleComm1.transition = 1 #Now we are in the transition state
            elif tracker1.voleComm1.transition == 1:
                tracker1.voleComm1.ping2 = 1
                print('RFID Ping 1-2 '+str(tracker1.voleComm2.ping2))
                tracker1.voleComm1.transition = 0

        if tracker1.voleTag2 in line_1.decode():
            print('Vole 2 Ping 1')
            if tracker1.voleComm2.transition == 0:
                tracker1.voleComm2.ping1 = 1
                tracker1.voleComm2.transition = 1
            elif tracker1.voleComm2.transition == 1:
                tracker1.voleComm2.ping2 = 1
                print('RFID Ping 2-2 '+str(tracker1.voleComm2.ping2))
                tracker1.voleComm2.transition = 0

        #This block of code waits until all threads are finished running to move on
        tracker1.event1.set() #Indicate that the thread is complete
        tracker1.mainEvent.wait()

def rfidTrack_2(eventDict,voleDict):
    serial_2 = serial.Serial(
        port = '/dev/ttySC1',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    # Set the tracker variables
    trackerVars = tracker()
    trackerVars.set_variables(eventDict, voleDict)

    while True:
        trackerVars.event2.clear()
        line_2 = serial_2.readline()
        # Print statements for debugging
        print("Line 2")
        print(line_2)
        if trackerVars.voleTag1 in line_2.decode(): 
            print('Vole 1 Ping 2')
            if trackerVars.voleComm1.transition == 0: #Entering transition
                trackerVars.voleComm1.ping1 = 3 #RFID number of the ping
                trackerVars.voleComm1.transition = 1 #Now we are in the transition state
            elif trackerVars.voleComm1.transition == 1:
                trackerVars.voleComm1.ping2 = 3
                print('RFID Ping 1-2 '+str(trackerVars.voleComm2.ping2))
                trackerVars.voleComm1.transition = 0
        if trackerVars.voleTag2 in line_2.decode():
            print('Vole 2 Ping 2')
            if trackerVars.voleComm2.transition == 0:
                trackerVars.voleComm2.ping1 = 3
                trackerVars.voleComm2.transition = 1
            elif trackerVars.voleComm2.transition == 1:
                trackerVars.voleComm2.ping2 = 3
                print('RFID Ping 2-2 '+str(trackerVars.voleComm2.ping2))
                trackerVars.voleComm2.transition = 0
        #This block of code waits until all threads are finished running to move on
        trackerVars.event2.set()
        trackerVars.mainEvent.wait()