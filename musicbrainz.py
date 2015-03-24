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
release_url = url + u'release-group/'
throttle = 1

useragent = u'media-artwork/0.0.1 ( https://github.com/varl/media-artwork )'

def search_artist(artist, albums):
  time.sleep(throttle) # wait for one second because of rate limits 

  data = dict(query='artist:'+artist.encode('utf-8'))
  req = urllib.urlencode(data)
  fullurl = artist_url +u'?'+ req
  #print fullurl
  request = urllib2.Request(fullurl, headers={"User-Agent" : useragent})
  xml = urllib2.urlopen(request).read()
  root = ET.fromstring(xml)
  
  artists = []
  for item in root[0]:
    if item[0].text == artist:
      mbid = item.get('id')
      name = item[0].text
      print u'Case sensitive match:\t{}\t{}'.format(name, artist)
      artists.append((mbid, name))
  
  candidate = None
  if len(artists) == 1:
    candidate = artists[0]
  else:
    for album in albums:
      for a_mbid, a_name in artists:
        print a_name, a_mbid, album.get('artist_mbid')
        if album.get('artist_mbid') == a_mbid:
          print u'Artist MBID from Album MBID match:\t{}\t{}'\
              .format(a_name, a_mbid)
          candidate = (a_name, a_mbid)
          break

  if candidate is None:
    print u'No album matches. Using first result for: {}'.format(artist)
    candidate = (root[0][0].get('id'), root[0][0][0].text)

  print candidate[0], '\t', candidate[1]
  return dict(mbid=candidate[0], name=candidate[1])

def search_releasegroup(title, year, artistname, dirname=''):
  time.sleep(throttle) # wait for one second because of rate limits 

  query = 'release:'+title.encode('utf-8')+' AND artist:'+artistname.encode('utf-8')

  data = dict(query=query)
  req = urllib.urlencode(data)
  fullurl = release_url +u'?'+ req
  #print fullurl
  request = urllib2.Request(fullurl, headers={"User-Agent" : useragent})
  xml = urllib2.urlopen(request).read()

  root = ET.fromstring(xml)
  for release in root[0]:
    mbid = release.get('id')
    name = release[0].text

    artist_credit = release.find('{http://musicbrainz.org/ns/mmd-2.0#}artist-credit')

    artist = artist_credit.find('{http://musicbrainz.org/ns/mmd-2.0#}name-credit').find('{http://musicbrainz.org/ns/mmd-2.0#}artist')
    artist_mbid = artist.get('id')
    album_artist = artist[0].text

    if album_artist == artistname and name == title:
      print mbid, '\t', year, '\t', name
      return dict(mbid=mbid, year=year, title=name, dirname=dirname,artist_mbid=artist_mbid)

    else:
      print u'The album artist does not match the directory artist:\t{}\t{}'\
          .format(album_artist, artistname)
      print u'And the name does not match the title:\t\t{}\t{}'\
          .format(name, title)

  return
