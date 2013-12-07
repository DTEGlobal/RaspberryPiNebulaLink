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

messageToSend = 'MD0'
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
    messageToSend = 'MD0'
    port.flushOutput()
    print("TxST: Error->[{}]".format(error))


def SendCommand():
    global tenSec, Rx, messageToSend, errorCounter, _38, _39

    print("TxST: SendCommand Thread Running ...")
    port.flushOutput()

    while True:
        if messageToSend == 'MD0':
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
                if MessageFromSerial[3] == 'D':
                    Rx = False
                    messageToSend = 'M1'
                    _39 = MessageFromSerial
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
    # TODO: Not in Tab code
    return 'N/A'


def getTodayRuntime():
    TodayRuntime = int(MB[38:42], 16)
    if bitState.getBitState(E[16:17], 1) == 'true':
        TodayRuntime += 65535
    return TodayRuntime


def getKickoffCount():
    return 0  # Not used


def getMessageNumber():
    return 0  # Not used


def getNoLoad():
    # TODO: Not in Tab code
    return 'N/A'


def getNoPosition():
    # TODO: Not in Tab code
    return 'N/A'


def getPercentFillage():
    # TODO: Not in Tab code
    return 'N/A'


def getPercentFillageSetting():
    return int(S_1[33:35], 16)*10


def getPumpOff():
    return bitState.getBitState(E[16:17], 2)


def getSecondsToNextStart():
    # TODO: ???? no minutes? ..
    return 'N/A'


def getSignalStrength():
    return 1  # Not used


def getStrokesLastCycle():
    return int(MB[42:46], 16)


def getStrokesThisCycle():
    return int(MB[25:29], 16)


def getTimeOut():
    return 256 - int(S_1[29:31], 16)


def getWellStatus():
    return bitState.getBitState(E[24:25], 3)

