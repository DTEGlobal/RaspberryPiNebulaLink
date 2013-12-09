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
import time

import G4_CPURPI01 as Petrolog

import xml.etree.ElementTree as myXML
import xml.etree.ElementTree as point


G4Command = ''
Command = False

def updateServer():

    global G4Command, Command

    while True:

        # Update Data
        time.sleep(2.5)
        UpdateStateData = myXML.parse('XMLs/UpdateStateData.xml')

        Automatic = UpdateStateData.getroot().find('Automatic')
        Automatic.text = Petrolog.getAutomaticStatus()

        Efficiency = UpdateStateData.getroot().find('Efficiency')
        Efficiency.text = Petrolog.getTodayRuntimePercent()

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

        req = urllib2.Request(url='http://petrologtest.intelectix.com/api/state',
                              data=myXML.tostring(UpdateStateData.getroot()),
                              headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})
        urllib2.urlopen(req)

        # Update Graph
        time.sleep(2.5)
        GraphData = myXML.parse('XMLs/GraphData.xml')
        points = GraphData.getroot().find("Points")

        dyna = Petrolog.getDyna()
        if dyna != '':
            for p in dyna:
                points.append(
                    point.fromstring(
                        '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays">'
                         +str(p[0])+','+str(p[1])+'</string>'))
            try:
                print points[0].text
                tempDyna = myXML.tostring(GraphData.getroot())
                print (tempDyna)

                req = urllib2.Request(url='http://petrologtest.intelectix.com/api/graph',
                                      data=tempDyna,
                                      headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})
                urllib2.urlopen(req)
            except IndexError as e:
                print "Empty XML"
        else:
            print 'Empty Dyna'

        # Command Pending?
        time.sleep(2.5)
        req = urllib2.Request(url='http://petrologtest.intelectix.com/api/command',
                                      headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})
        resp = urllib2.urlopen(req)
        s = resp.read()
        respuesta = myXML.ElementTree(myXML.fromstring(s))

        commands = respuesta.iter(tag='Command')
        for command in commands:
            print command.text
            Command = True
            G4Command = command.text


        commandsIds = respuesta.iter(tag='ConsoleCommandId')
        for commandId in commandsIds:
            print commandId.text
            id = commandId.text
            while Petrolog.responseToServer == '':
                time.sleep(.01)

            req = urllib2.Request(url='http://petrologtest.intelectix.com/api/command',
                                         data='<CommandResponse>'
                                                    '<ConsoleCommandId>'
                                                        +id+
                                                    '</ConsoleCommandId>'
                                                    '<Response>'
                                                        +Petrolog.responseToServer+
                                                    '</Response>'
                                              '</CommandResponse>',
                                         headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})

            Petrolog.responseToServer = ''
            resp = urllib2.urlopen(req)
            print id+"....."
            print resp.read()

