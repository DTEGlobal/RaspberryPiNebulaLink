__author__ = 'Cesar'

import threading
import time
import G4_CPURPI01
import xmlUpdater
import apiClient

SerialRxThread = threading.Thread(target=G4_CPURPI01.SendCommand)
SerialRxThread.daemon = True
SerialRxThread.start()

time.sleep(5)
updateXMLThread = threading.Thread(target=xmlUpdater.updateXML)
updateXMLThread.daemon = True
updateXMLThread.start()

time.sleep(1)
updateServer = threading.Thread(target=apiClient.updateServer())
updateServer.daemon = True
updateServer.start()

while True:
    a=0 #Do nothing
