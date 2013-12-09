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

import xml.etree.ElementTree as myXML
import xml.etree.ElementTree as point

import G4_CPURPI01 as Petrolog

GraphData = myXML.parse('XMLs/GraphData.xml')
UpdateStateData = myXML.parse('XMLs/UpdateStateData.xml')

processingDyna = False

def updateXML():

    while True:

        global UpdateStateData

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




        global GraphData, processingDyna


        GraphData = myXML.parse('XMLs/GraphData.xml')
        points = GraphData.getroot().find("Points")

        dyna = Petrolog.getDyna()

        try:
            print points[0].text
        except IndexError as e:
            if dyna != '':
                processingDyna = True
                for p in dyna:
                    points.append(
                        point.fromstring(
                            '<string xmlns="http://schemas.microsoft.com/2003/10/Serialization/Arrays">'
                             +str(p[0])+','+str(p[1])+'</string>'))
                processingDyna = False
