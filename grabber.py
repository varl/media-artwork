#-*- coding: utf-8 -*-
import os
import os.path
import codecs
import sys
import re
import urllib

import fanarttv

from meta import music_meta, movie_meta, tv_meta, scan_media
from config import Config

def scan_music(path):
  data = []
  dirs = scan_media(path)
  for d in dirs:
    meta = music_meta(path, d)
    data = fanarttv.music_art(meta)
  return data

def scan_movie(path):
  data = []
  dirs = scan_media(path)
  for d in dirs:
    meta = movie_meta(path, d)
    data.extend(fanarttv.movie_art(meta))
  return data

def scan_tv(path):
  data = []
  dirs = scan_media(path)
  for d in dirs:
    meta = tv_meta(path, d)
    data = fanarttv.tv_art(meta)
  return data

def download(data):
    for local, remote in data:
      if os.path.exists(local):
        print u'Local file exists ({}), skipping...'.format(local)
      else:
        print u'Downloading\t{}'.format(remote)
        filename, headers = urllib.urlretrieve(remote, local)
        print u'Downloaded\t{}'.format(filename)
  

if __name__ == "__main__":
  UTF8Writer = codecs.getwriter('utf8')
  sys.stdout = UTF8Writer(sys.stdout)

  cfg = Config()
  paths = cfg.paths

  data = []
  for category, path in paths.iteritems():
    if category == "music":
      data.extend(scan_music(path))
    elif category == "tv":
      data.extend(scan_tv(path))
    else:
      data.extend(scan_movie(path))

  print data
  download(data)
