__author__ = 'Cesar'

#-------------------------------------------------------------------------------
# Name:        G4Test
# Purpose:
#
# Author:      Cesar
#
# Created:     07/08/2013
# Copyright:   (c) Cesar 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import serial
import threading

messageToSend = 'E'
tenSec = 0
Rx = True
errorCounter = 0

def SendCommand():
    global tenSec, Rx, messageToSend, errorCounter

    print("TxST: SendCommand Thread Running ...")
    port.flushOutput()


    while True:
        if messageToSend == 'E':
            command = "01E\x0D"
            Rx = True
        elif messageToSend == 'MB':
            command = "01MB\x0D"
            Rx = True
        elif messageToSend == 'S?1':
            command = "01S?1\x0D"
            Rx = True

        data_toPrint = command[:-1]
        print("[{}]TxST: Tx Data->[{}]".format(time.clock(), data_toPrint))
        port.write(command)
        while Rx:
            try:
                MessageFromSerial = port.readline()
                # Remove last 3 chars (CR LF)
                data_toPrint = MessageFromSerial[:-2]
                print("[{}]RxST: Rx Data->[{}]".format(time.clock(), data_toPrint))
                Rx = False

            except serial.SerialException as e:
                print("Error: ..."+e)

            except IndexError as i:
                print("Error: ..."+i)




global port

port = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=1)

SerialRxThread = threading.Thread(target=SendCommand)
SerialRxThread.daemon = True
SerialRxThread.start()

while True:
    a=0 #Do nothing