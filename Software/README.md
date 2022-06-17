# Software Dev
This outlines the necessary steps to setup and run the software package for a given homecage experiment.

## Raspberry Pi Setup
It is best here to start with a clean install of the Raspbian software. When installing it is recommended to use the Raspberry Pi Imager found [here](https://www.raspberrypi.com/software/). When installing the OS using this software, make sure to select the more options button, and setup a user, as well as enabling ssh privileges for the OS install.

With the OS installed, boot up the Pi while connected to an external monitor, keyboard, and mouse. This way you can get the current IP address of the pi to be able to ssh into it from another machine. Once this is done, the next steps can all be performed through SSH from a remote machine.

### Setting up CAN bus utils
The RFID antennas in the project communicate with the raspberry pi through a communications scheme known as CANbus. There are a few steps that need to be taken in order to set up this functionality on the pi.

After making sure the pi OS is completely up to date, the following lines of code need to be added to the end of the boot file located in /boot/config.txt:

`dtparam=spi=on`  
`dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25`  
`dtoverlay=spi-bcm2835-overlay`  

And then reboot the pi for the commands to take effect.

To get the necessary python library, [python-can](https://python-can.readthedocs.io/en/master/) just run the install command for the library:  

`pip3 install python-can`  

Note that the import call in a `.py` file will be `import can` and NOT `import python-can`. 

If desired, you can read a full [user guide](https://copperhilltech.com/pican2-controller-area-network-can-interface-for-raspberry-pi/) for the specific piece of hardware, and if you run into issues with reading and/or writing CAN signals the manufacturer also has a [troubleshooting document](https://copperhilltech.com/blog/troubleshooting-your-pican2-can-interface-board-for-raspberry-pi/) to read. 

### Downloading the software package
Downloading the software package is relatively, simply clone [this git repository](https://github.com/donaldsonlab/Home_Cage/tree/master) into the home directory of the raspberry pi. Then, you can test the CAN functionality by hooking up the pi to the arduino tester and monitoring the CAN signal. This test can be run by running the file named `test_can.py`. 
