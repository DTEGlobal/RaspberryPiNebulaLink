__author__ = 'Cesar'

import threading
import time
import G4_CPURPI01
import apiClient

SerialRxThread = threading.Thread(target=G4_CPURPI01.SendCommand)
SerialRxThread.daemon = True
SerialRxThread.start()

time.sleep(5)
updateServer = threading.Thread(target=apiClient.updateServer())
updateServer.daemon = True
updateServer.start()

while True:
    a=0 #Do nothing
