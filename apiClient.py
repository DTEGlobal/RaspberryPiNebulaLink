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

import G4_CPURPI01
import xmlUpdater


import xml.etree.ElementTree as myXML

G4Command = ''
Command = False

def updateServer():

    global G4Command, Command

    while True:

        # Update Data
        time.sleep(2.5)
        req = urllib2.Request(url='http://petrologtest.intelectix.com/api/state',
                              data=xmlUpdater.myXML.tostring(xmlUpdater.UpdateStateData.getroot()),
                              headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})
        urllib2.urlopen(req)

        # Update Graph
        time.sleep(2.5)
        while xmlUpdater.processingDyna:
            time.sleep(.01)
        try:
            print xmlUpdater.GraphData.getroot().find('Points')[0].text
            tempDyna = xmlUpdater.myXML.tostring(xmlUpdater.GraphData.getroot())
            print (tempDyna)
            req = urllib2.Request(url='http://petrologtest.intelectix.com/api/graph',
                                  data=tempDyna,
                                  headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})
            urllib2.urlopen(req)
            for child in xmlUpdater.GraphData.getroot().find('Points'):
                xmlUpdater.GraphData.getroot().find('Points').remove(child)
        except IndexError as e:
            print "Empty XML"

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
            while G4_CPURPI01.responseToServer == '':
                time.sleep(.01)

            req = urllib2.Request(url='http://petrologtest.intelectix.com/api/command',
                                         data='<CommandResponse>'
                                                    '<ConsoleCommandId>'
                                                        +id+
                                                    '</ConsoleCommandId>'
                                                    '<Response>'
                                                        +G4_CPURPI01.responseToServer+
                                                    '</Response>'
                                              '</CommandResponse>',
                                         headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})

            G4_CPURPI01.responseToServer = ''
            resp = urllib2.urlopen(req)
            print id+"....."
            print resp.read()

