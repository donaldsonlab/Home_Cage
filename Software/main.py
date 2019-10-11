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
