# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import os
import collections
import time

import xml.etree.ElementTree as ET

url = u'http://musicbrainz.org/ws/2/'
artist_url = url + u'artist/'
release_url = url + u'release/'
throttle = 1

useragent = u'media-artwork/0.0.1 ( https://github.com/varl/media-artwork )'

def search_artist(artist):
  time.sleep(throttle) # wait for one second because of rate limits 

  data = dict(query='artist:'+artist)
  req = urllib.urlencode(data)
  fullurl = artist_url +u'?'+ req
  print fullurl
  request = urllib2.Request(fullurl, headers={"User-Agent" : useragent})
  xml = urllib2.urlopen(request).read()
  root = ET.fromstring(xml)
  
  mbid = root[0][0].get('id')
  name = root[0][0][0].text

  return dict(mbid=mbid, name=name)

def search_release(title, year):
  time.sleep(throttle) # wait for one second because of rate limits 

  data = dict(query=u'name:'+title.encode('ascii', 'ignore'))
  req = urllib.urlencode(data)
  fullurl = release_url +u'?'+ req
  print fullurl
  request = urllib2.Request(fullurl, headers={"User-Agent" : useragent})
  xml = urllib2.urlopen(request).read()

  root = ET.fromstring(xml)
  mbid = root[0][0].get('id')
  name = root[0][0][0].text

  print mbid, year, name
  return dict(mbid=mbid, year=year, title=name)
