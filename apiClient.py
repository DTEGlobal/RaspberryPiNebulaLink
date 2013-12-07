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
import xmlUpdater
import time

def updateServer():
    while True:
        time.sleep(15)
        req = urllib2.Request(url='http://petrologtest.intelectix.com/api/graph',
                              data=xmlUpdater.myXML.tostring(xmlUpdater.GraphData.getroot()),
                              headers={'Content-Type':'text/xml','Authorization':'DeviceNumber=19,ApiKey=test'})
        urllib2.urlopen(req)

