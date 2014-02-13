__author__ = 'Cesar'

#-------------------------------------------------------------------------------
# Name:        apiClient
# Purpose:
#
# Author:      Cesar
#
# Created:     12/04/2013
# Copyright:   (c) Cesar 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib2
from urllib2 import URLError
import time

import G4_CPURPI01 as Petrolog

import xml.etree.ElementTree as myXML
import xml.etree.ElementTree as point

import uuid
import Feeder

import logging

G4Command = ''
Command = False


def updateServer():

    global G4Command, Command

    apiId = str(uuid.uuid4())
    data_toPrint = "updateServer: updateServer Thread Running ..."

    while True:

        # Update Data
        time.sleep(2.5)
        UpdateStateData = myXML.parse('/home/pi/api/XMLs/UpdateStateData.xml')

        try:

            Automatic = UpdateStateData.getroot().find('Automatic')
            Automatic.text = Petrolog.getAutomaticStatus()

            Efficiency = UpdateStateData.getroot().find('Efficiency')
            if int(Petrolog.getTodayRuntimePercent()) < 100:
                Efficiency.text = Petrolog.getTodayRuntimePercent()
            else:
                Efficiency.text = '100'


            KickoffCount = UpdateStateData.getroot().find('KickoffCount')
            KickoffCount.text = Petrolog.getKickoffCount()

            MessageNumber = UpdateStateData.getroot().find('MessageNumber')
            MessageNumber.text = Petrolog.getMessageNumber()

            NoLoad = UpdateStateData.getroot().find('NoLoad')
            NoLoad.text = Petrolog.getNoLoad()

            NoPosition = UpdateStateData.getroot().find('NoPosition')
            NoPosition.text = Petrolog.getNoPosition()

            PercentFillage = UpdateStateData.getroot().find('PercentFillage')
            PercentFillage.text = Petrolog.getPercentFillage()

            PercentFillageSetting = UpdateStateData.getroot().find('PercentFillageSetting')
            PercentFillageSetting.text = Petrolog.getPercentFillageSetting()

            PumpOff = UpdateStateData.getroot().find('PumpOff')
            PumpOff.text = Petrolog.getPumpOff()

            SecondsToNextStart = UpdateStateData.getroot().find('SecondsToNextStart')
            SecondsToNextStart.text = Petrolog.getSecondsToNextStart()

            SignalStrength = UpdateStateData.getroot().find('SignalStrength')
            SignalStrength.text = Petrolog.getSignalStrength()

            StrokesLastCycle = UpdateStateData.getroot().find('StrokesLastCycle')
            StrokesLastCycle.text = Petrolog.getStrokesLastCycle()

            StrokesThisCycle = UpdateStateData.getroot().find('StrokesThisCycle')
            StrokesThisCycle.text = Petrolog.getStrokesThisCycle()

            TimeOut = UpdateStateData.getroot().find('TimeOut')
            TimeOut.text = Petrolog.getTimeOut()

            WellStatus = UpdateStateData.getroot().find('WellStatus')
            WellStatus.text = Petrolog.getWellStatus()

        except ValueError:
            logging.error('State Data Update - Serial communications failure')

        req = urllib2.Request(url='http://petrolog.intelectix.com/api/state',
                              data=myXML.tostring(UpdateStateData.getroot()),
                              headers={'Content-Type':'text/xml',
                                       'Authorization':'DeviceNumber=1943,ApiKey=UGV0cm9sb2dDbGllbnRl'})
        try:
            resp = urllib2.urlopen(req)
        except URLError as e:
            logging.warning('State Data Update - Failed to open connection to server! Error = %s', e.reason)
        else:
            r = resp.read()
            respuesta = myXML.ElementTree(myXML.fromstring(r))
            if respuesta.getroot().getiterator()[3].text == 'true':
                # Feed Watchdog Server only if request OK
                Feeder.feeder(apiId, data_toPrint)

        # Update Graph
        time.sleep(2.5)
        GraphData = myXML.parse('/home/pi/api/XMLs/GraphData.xml')
        points = GraphData.getroot().find("Points")

        dyna = Petrolog.getDyna()
        if dyna != '':
            for p in dyna:
                points.append(
                    point.fromstring(
                        '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays">'
                         +str(p[0])+','+str(p[1])+'</string>'))
            try:
                tempDyna = myXML.tostring(GraphData.getroot())
                req = urllib2.Request(url='http://petrolog.intelectix.com/api/graph',
                                      data=tempDyna,
                                      headers={'Content-Type':'text/xml',
                                               'Authorization':'DeviceNumber=1943,ApiKey=UGV0cm9sb2dDbGllbnRl'})
                try:
                    urllib2.urlopen(req)
                except URLError as e:
                    logging.warning('Dyna Update - Failed to open connection to server! Error = %s', e.reason)
            except IndexError:
                logging.warning('Dyna Update - Empty XML')

        # Command Pending?
        time.sleep(2.5)
        req = urllib2.Request(url='http://petrolog.intelectix.com/api/command',
                                      headers={'Content-Type':'text/xml',
                                               'Authorization':'DeviceNumber=1943,ApiKey=UGV0cm9sb2dDbGllbnRl'})
        try:
            resp = urllib2.urlopen(req)
            s = resp.read()
            respuesta = myXML.ElementTree(myXML.fromstring(s))

            commands = respuesta.iter(tag='Command')
            for command in commands:
                print 'Command from server: '+command.text
                Command = True
                G4Command = command.text
            commandsIds = respuesta.iter(tag='ConsoleCommandId')
            for commandId in commandsIds:
                print 'Command ID: '+commandId.text
                id = commandId.text
                while Petrolog.responseToServer == '':
                    time.sleep(.01)
                req = urllib2.Request(url='http://petrolog.intelectix.com/api/command',
                                             data='<CommandResponse>'
                                                        '<ConsoleCommandId>'
                                                            +id+
                                                        '</ConsoleCommandId>'
                                                        '<Response>'
                                                            +Petrolog.responseToServer+
                                                        '</Response>'
                                                  '</CommandResponse>',
                                             headers={'Content-Type':'text/xml',
                                                      'Authorization':'DeviceNumber=1943,ApiKey=UGV0cm9sb2dDbGllbnRl'})

                Petrolog.responseToServer = ''
                urllib2.urlopen(req)

        except URLError as e:
            logging.warning('Console Command - Failed to open connection to server! Error = %s', e.reason)
