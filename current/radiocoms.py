from threading import Thread
import asteroids
import time
import sys
import signal
from rpi_rf import RFDevice     #imports 433mhz framework

class inputScanner:
    def __init__(self):
        self.running = True
        self.inputList = []     #Saves every input command into a list that is used by handle_inputs()
        self.isLocked = False       # The list is most likely not going to contain more than 1 command but it is a safer way
        self.rfdevice = RFDevice(23)  # Sets listening GPIO pin to 23
        self.rfdevice.enable_rx()  # Enables the receiver
        self.commands = (1000, 2000, 3000, 4000, 5000, 10000, 11000, 12000, 13000, 14000, 15000, 16000) #Using tuples since these should not be changed when running
        signal.signal(signal.SIGINT, self.exithandler)

    def terminate(self):
        self.running = False    #Kill function

    def exithandler(self, signal, frame):
        self.rfdevice.cleanup()
        sys.exit(0)

    def run(self):
        while self.running:                 #This thread is going to listen at all times to the rf receiver
            rfValue = int(self.rfdevice.rx_code or 0)        #Forces the read value into an int. if value is none read it as 0
            if (rfValue in self.commands and self.isLocked != True):      #Checks if the received value is in the accepted command list and that the list is not locked.
                #print(rfValue)
                self.isLocked = True
                self.inputList.append(rfValue)     #Saves input into the list
                self.isLocked = False
                #time.sleep(0.01)                                #waits 0.01s to cap the refresh rate
            #else:                                           #if it is just jitter, wait for another loop
                #time.sleep(0.01)
        self.rfdevice.cleanup()