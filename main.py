__author__ = 'Cesar'

import threading
import time
import G4_CPURPI01
import apiClient
import logging

logging.basicConfig(format='%(asctime)s - [%(levelname)s]: %(message)s',
                    filename='/home/pi/logs/api.log',
                    level=logging.INFO)
logging.info('Watchdog main - Started')

SerialRxThread = threading.Thread(target=G4_CPURPI01.SendCommand)
SerialRxThread.daemon = True
SerialRxThread.start()

time.sleep(5)
updateServer = threading.Thread(target=apiClient.updateServer())
updateServer.daemon = True
updateServer.start()

while True:
    a = 0  # Do nothing

