# -*- coding: utf-8 -*-
import os
import os.path
import codecs
import sys
import re

from config import Config
from omdbapi import search

def movie_meta(dirname):
    pattern = re.compile(ur'(?P<title>^.*)\s\((?P<year>\d{4})\)', re.U)
    match = re.search(pattern, dirname)
    match.groups()

    title = match.group('title')
    year = match.group('year')
    
    movie = search(title=title, type='movie')

    return dict(dirname=dirname, year=year, title=title)

def scan_music(target):
    pass

def scan_movies(target):
    return movie_meta(target)

def scan_tv(target):
    pass

def scan_media(target):
  print 'Scanning %s' % target
  dirlist = [d for d in os.listdir(target) if os.path.isdir(os.path.join(target, d))]
  return dirlist
  

if __name__ == "__main__":

  cfg = Config()
  paths = cfg.paths
  media = {}
        
  for category in cfg.categories:
    media[category] = []
    dirs = scan_media(paths.get(category))

    if category == "music":
        scanner = scan_music
    elif category == "tv":
        scanner = scan_tv
    else:
        scanner = scan_movies

    for d in dirs:
        media[category].append(scanner(d))

