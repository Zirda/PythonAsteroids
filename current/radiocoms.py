from threading import Thread
import time
from rpi_rf import RFDevice     #imports 433mhz framework

rfdevice = RFDevice(23)         #Sets listening GPIO pin to 23
rfdevice.enable_rx()            #Enables the receiver

class inputScanner:
    def __init__(self):
        self.running = True
        self.inputList = []     #Saves every input command into a list that is used by handle_inputs()
                                # The list is most likely not going to contain more than 1 command but it is a safer way

    def terminate(self):
        self.running = False    #Kill function

    def run(self):
        while True:                 #This thread is going to listen at all times to the rf receiver
            rfValue = int(rfdevice.rx_code or 0)        #Forces the read value into an int. if value is none read it as 0
            if (rfValue % 1000 == 0 and rfValue != 0):      #Every command broadcasted with be in the equal 1000 so using modolus 1000 it filters out a lot of jitter
                self.inputList.append(rfdevice.rx_code)     #Saves input into the list
                time.sleep(0.01)                                #waits 0.01s to cap the refresh rate
            else:                                           #if it is just jitter, wait for another loop
                time.sleep(0.01)
            #rfdevice.cleanup()                                  #empties the saved value from rfdevice.rx_code