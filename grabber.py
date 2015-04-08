#-*- coding: utf-8 -*-
import os
import os.path
import codecs
import sys
import re
import urllib

import fanarttv

from meta import music_meta, movie_meta, tv_meta
from config import Config

def scan_music(path, target):
    meta = music_meta(path, target)
    data = fanarttv.music_art(meta)
    return download(data)

def scan_movie(path, target):
    pass
    meta = movie_meta(path, target)
    data = fanarttv.movie_art(meta)
    return download(data)

def scan_tv(path, target):
    meta = tv_meta(path, target)
    data = fanarttv.tv_art(meta)
    return download(data)

def scan_media(target):
  if not os.path.isdir(target):
    print u'Path does not exist, skipping {}'.format(target)
    return []

  print u'Scanning {}'.format(target)
  dirlist = [d for d in os.listdir(target) if os.path.isdir(os.path.join(target, d))]
  return dirlist

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

    for category in cfg.categories:
        dirs = scan_media(paths.get(category))

        if category == "music":
            populate = scan_music
        elif category == "tv":
            populate = scan_tv
        else:
            populate = scan_movie

        for d in dirs:
            populate(paths.get(category), d)

