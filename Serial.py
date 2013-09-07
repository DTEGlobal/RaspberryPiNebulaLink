__author__ = 'Cesar'

#-------------------------------------------------------------------------------
# Name:        Serial
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

def stopO():
    port.write("01S?1\x0D\x0A")
    foo = port.readline()
    print ("TxST: Stop O->[{}]".format(foo))
    time.sleep(1)


def errorCleanUp(error):
    global tenSec, Rx, messageToSend, errorCounter

    tenSec = 0
    errorCounter = 0
    Rx = False
    messageToSend = 'E'
    port.flushOutput()
    print ("TxST: Error->[{}]".format(error))


def SendCommand():
    global tenSec, Rx, messageToSend, errorCounter

    print ("TxST: SendCommand Thread Running ...")
    port.flushOutput()

    cycleStart = time.clock()

    while True:
        if messageToSend == 'E':
            command = "01E\x0D"
            Rx = True
        elif messageToSend == 'MB':
            command = "01MB\x0D"
            Rx = True
        elif messageToSend == 'O':
            if (time.clock() - cycleStart) > 10:
                command = "01O\x0D"
                Rx = True
            else:
                command = "01E\x0D"
                Rx = True
        elif messageToSend == 'S?1':
            command = "01S?1\x0D"
            Rx = True

        data_toPrint = command[:-1]
        print ("[{}]TxST: Tx Data->[{}]".format(time.clock(),data_toPrint))
        port.write(command)
        while Rx:
            try:
                MessageFromSerial = port.readline()
                # Remove last 3 chars (CR LF)
                data_toPrint = MessageFromSerial[:-2]
                print ("[{}]RxST: Rx Data->[{}]".format(time.clock(),data_toPrint))
                # Check Rx contents
                if MessageFromSerial[3] == 'E':
                    Rx = False
                    messageToSend = 'MB'
                elif MessageFromSerial[3] == 'M':
                    Rx = False
                    messageToSend = 'O'
                elif MessageFromSerial[13:15] == ',,':
                    tenSec += 1
                    if tenSec >= 3:
                        tenSec = 0
                        errorCounter = 0
                        Rx = False
                        messageToSend = 'S?1'
                        stopO()
                        cycleStart = time.clock()
                elif MessageFromSerial[2] == 'S':
                    Rx = False
                    messageToSend = 'E'
                else:
                    if messageToSend == 'O':
                        errorCounter += 1
                        if errorCounter >= 2:
                            errorCleanUp("More than 2 errors in O")
                    else:
                        errorCleanUp(MessageFromSerial)


            except serial.SerialException as e:
                errorCleanUp(e)

            except IndexError as i:
                errorCleanUp(i)




global port

port = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=1)

SerialRxThread = threading.Thread(target=SendCommand)
SerialRxThread.daemon = True
SerialRxThread.start()

while True:
    a=0 #Do nothing
