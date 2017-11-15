from threading import Thread
import time
from rpi_rf import RFDevice

rfdevice = None

rfdevice = RFDevice(23)
rfdevice.enable_rx()

class inputScanner:
    def __init__(self):
        self.running = True
        self.inputList = []

    def terminate(self):
        self.running = False

    def run(self):
        while True:
            rfValue = int(rfdevice.rx_code or 0)
            if (rfValue % 1000 == 0 and rfValue != 0):
                self.inputList.append(rfdevice.rx_code)
                time.sleep(0.01)
            else:
                time.sleep(0.01)
        rfdevice.cleanup()