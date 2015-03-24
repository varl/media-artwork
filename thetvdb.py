# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import os
import collections

import xml.etree.ElementTree as ET

url = u'http://thetvdb.com/api'
api_key = u'ED0FD39C9529CF14'

# GetSeries.php?seriesname=<seriesname>
# GetSeriesByRemoteID.php?imdbid=<imdbid>

def search(term):
    data = dict(seriesname=term)
    req = urllib.urlencode(data)
    fullurl = url + u'/GetSeries.php?' + req
    xml = urllib2.urlopen(fullurl).read()
    return ET.fromstring(xml)

def remote_id(imdbid):
    data = dict(imdbid=imdbid)
    req = urllib.urlencode(data)
    fullurl = url + u'/GetSeriesByRemoteID.php?' + req
#    print fullurl
    xml = urllib2.urlopen(fullurl).read()
#    print xml
    return ET.fromstring(xml)
    
