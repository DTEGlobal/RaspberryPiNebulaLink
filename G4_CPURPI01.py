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
import bitState
import apiClient

messageToSend = 'Config'
responseToServer = ''
tenSec = 0
Rx = True
errorCounter = 0

_39 = ''
_38 = ''

global port

port = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=1)


def errorCleanUp(error):
    global tenSec, Rx, messageToSend, errorCounter

    tenSec = 0
    errorCounter = 0
    Rx = False
    messageToSend = 'Config'
    port.flushOutput()
    print("TxST: Error->[{}]".format(error))


def SendCommand():
    global tenSec, Rx, messageToSend, errorCounter, _38, _39, responseToServer

    print("TxST: SendCommand Thread Running ...")
    port.flushOutput()

    waitingForConsoleCommand = False

    while True:
        if apiClient.Command:
            command = apiClient.G4Command+"\x0D"
            waitingForConsoleCommand = True
            Rx = True
        elif messageToSend == 'Config':
            command = "00SZ50132\x0D"
            Rx = True
        elif messageToSend == 'MD0':
            command = "00MD0\x0D"
            Rx = True
        elif messageToSend == 'M1':
            command = "00M1\x0D"
            Rx = True
        elif messageToSend == 'M2':
            command = "00M2\x0D"
            Rx = True
        elif messageToSend == 'M3':
            command = "00M3\x0D"
            Rx = True
        elif messageToSend == 'M4':
            command = "00M4\x0D"
            Rx = True
        elif messageToSend == 'M5':
            command = "00M5\x0D"
            Rx = True
        elif messageToSend == 'M6':
            command = "00M6\x0D"
            Rx = True
        elif messageToSend == 'M7':
            command = "00M7\x0D"
            Rx = True
        elif messageToSend == 'M8':
            command = "00M8\x0D"
            Rx = True

        data_toPrint = command[:-1]
        # print("[{}]TxST: Tx Data->[{}]".format(time.clock(), data_toPrint))
        port.write(command)
        while Rx:
            try:
                MessageFromSerial = port.readline()
                # Remove last 3 chars (CR LF)
                data_toPrint = MessageFromSerial[:-2]
                # print("[{}]RxST: Rx Data->[{}]".format(time.clock(), data_toPrint))
                # Check Rx contents
                if waitingForConsoleCommand:
                    Rx = False
                    messageToSend = 'MD0'
                    if MessageFromSerial == '':
                        responseToServer = 'Error: Time Out'
                    else:
                        responseToServer = MessageFromSerial[:-2]
                    print ('Console Command Response: '+responseToServer)
                    waitingForConsoleCommand = False
                    apiClient.Command = False
                elif MessageFromSerial[3] == 'Z':
                    Rx = False
                    messageToSend = 'MD0'
                    print ('Configured! '+MessageFromSerial)
                elif MessageFromSerial[3] == 'D':
                    Rx = False
                    messageToSend = 'M1'
                    _39 = MessageFromSerial[5:]
                elif MessageFromSerial[3] == '1':
                    Rx = False
                    messageToSend = 'M2'
                    _38 = ""
                    _38 = MessageFromSerial[12:-2]
                elif MessageFromSerial[3] == '2':
                    Rx = False
                    messageToSend = 'M3'
                    _38 = _38 + MessageFromSerial[4:-2]
                elif MessageFromSerial[3] == '3':
                    Rx = False
                    messageToSend = 'M4'
                    _38 = _38 + MessageFromSerial[4:-2]
                elif MessageFromSerial[3] == '4':
                    Rx = False
                    messageToSend = 'M5'
                    _38 = _38 + MessageFromSerial[4:-2]
                elif MessageFromSerial[3] == '5':
                    Rx = False
                    messageToSend = 'M6'
                    _38 = _38 + MessageFromSerial[4:-2]
                elif MessageFromSerial[3] == '6':
                    Rx = False
                    messageToSend = 'M7'
                    _38 = _38 + MessageFromSerial[4:-2]
                elif MessageFromSerial[3] == '7':
                    Rx = False
                    messageToSend = 'M8'
                    _38 = _38 + MessageFromSerial[4:-2]
                elif MessageFromSerial[3] == '8':
                    Rx = False
                    messageToSend = 'MD0'
                    _38 = _38 + MessageFromSerial[4:-2]
                else:
                    errorCleanUp(MessageFromSerial)

            except serial.SerialException as e:
                errorCleanUp(e)

            except IndexError as i:
                errorCleanUp(i)

def getDyna():
    global _38
    char = 0
    dyna = [(0, 0)]
    dyna.pop(0)
    while True:
        if (_38[char:char+4] == '') or (_38[char+4:char+4+4] == ''):
            return ''
        elif (_38[char:char+4] == 'FFFF') or (_38[char+4:char+4+4] == 'FFFF'):
            return dyna
        else:
            try:
                pair = (int(_38[char:char+4], 16), int(_38[char+4:char+4+4], 16))
                dyna.append(pair)
                char += 8
            except ValueError as e:
                return ''


def getAutomaticStatus():
    return bitState.getBitState(_39[14:16], 1)


def getTime():
    hours = int(_39[20:22])
    min = int(_39[22:24])

    return (hours*3600)+(min*60)


def getTodayRuntimePercent():
    TodayRuntime = int(_39[52:56], 16)
    if bitState.getBitState(_39[18:20], 1) == 'true':
        TodayRuntime += 65535
    try:
        return str((TodayRuntime*100)/getTime())
    except ZeroDivisionError:
        return 'error'


def getKickoffCount():
    return '0'  # Not used


def getMessageNumber():
    return '0'  # Not used


def getNoLoad():
    return bitState.getBitState(_39[14:16], 2)


def getNoPosition():
    return bitState.getBitState(_39[14:16], 3)


def getPercentFillage():
    return str(int(_39[34:36], 16))


def getPercentFillageSetting():
    return str(int(_39[36:38])*10)


def getPumpOff():
    return bitState.getBitState(_39[18:20], 2)


def getSecondsToNextStart():
    return str(65535 - int(_39[64:68], 16))


def getSignalStrength():
    return '0'  # Not used


def getStrokesLastCycle():
    return str(int(_39[56:60], 16))


def getStrokesThisCycle():
    return str(int(_39[40:44], 16))


def getTimeOut():
    return str(256 - int(_39[48:50], 16))


def getWellStatus():
    if bitState.getBitState(_39[12:14], 7) == 'true':
        return 'false'
    else:
        return 'true'

