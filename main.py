__author__ = 'Cesar'

import threading

import G4_CPURPI01
import xmlUpdater
import apiClient

SerialRxThread = threading.Thread(target=G4_CPURPI01.SendCommand)
SerialRxThread.daemon = True
SerialRxThread.start()

updateXMLThread = threading.Thread(target=xmlUpdater.updateXML)
updateXMLThread.daemon = True
updateXMLThread.start()

updateServer = threading.Thread(target=apiClient.updateServer())
updateServer.daemon = True
updateServer.start()

while True:
    a=0 #Do nothing
