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
import time
import G4_CPURPI01 as Petrolog

GraphData = myXML.parse('XMLs/GraphData.xml')


def updateXML():

    while True:

        time.sleep(10)

        #UpdateStateData = myXML.parse('XMLs/UpdateStateData.xml')
        #
        #Automatic = UpdateStateData.getroot().find('Automatic')
        #Automatic.text = Petrolog.getAutomaticStatus()
        #
        #Efficiency = UpdateStateData.getroot().find('Efficiency')
        #Efficiency.text = Petrolog.getTodayRuntime()
        #
        #KickoffCount = UpdateStateData.getroot().find('KickoffCount')
        #KickoffCount.text = Petrolog.getKickoffCount()
        #
        #MessageNumber = UpdateStateData.getroot().find('MessageNumber')
        #MessageNumber.text = Petrolog.getMessageNumber()
        #
        #NoLoad = UpdateStateData.getroot().find('NoLoad')
        #NoLoad.text = Petrolog.getNoLoad()
        #
        #NoPosition = UpdateStateData.getroot().find('NoPosition')
        #NoPosition.text = Petrolog.getNoPosition()
        #
        #PercentFillage = UpdateStateData.getroot().find('PercentFillage')
        #PercentFillage.text = Petrolog.getPercentFillage()
        #
        #PercentFillageSetting = UpdateStateData.getroot().find('PercentFillageSetting')
        #PercentFillageSetting.text = Petrolog.getPercentFillageSetting()
        #
        #PumpOff = UpdateStateData.getroot().find('PumpOff')
        #PumpOff.text = Petrolog.getPumpOff()
        #
        #SecondsToNextStart = UpdateStateData.getroot().find('SecondsToNextStart')
        #SecondsToNextStart.text = Petrolog.getSecondsToNextStart()
        #
        #SignalStrength = UpdateStateData.getroot().find('SignalStrength')
        #SignalStrength.text = Petrolog.getSignalStrength()
        #
        #StrokesLastCycle = UpdateStateData.getroot().find('StrokesLastCycle')
        #StrokesLastCycle.text = Petrolog.getStrokesLastCycle()
        #
        #StrokesThisCycle = UpdateStateData.getroot().find('StrokesThisCycle')
        #StrokesThisCycle.text = Petrolog.getStrokesThisCycle()
        #
        #TimeOut = UpdateStateData.getroot().find('TimeOut')
        #TimeOut.text = Petrolog.getTimeOut()
        #
        #WellStatus = UpdateStateData.getroot().find('WellStatus')
        #WellStatus.text = Petrolog.getWellStatus()

        global GraphData

        GraphData = myXML.parse('XMLs/GraphData.xml')
        points = GraphData.getroot().find("Points")

        for child in points:
            point = child
            points.remove(child)

        dyna = Petrolog.getDyna()

        if dyna != '':
            for p in dyna:
                point.text = str(p[0])+','+str(p[1])
                points.append(point)

