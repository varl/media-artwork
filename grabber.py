# -*- coding: utf-8 -*-
import os
import os.path
import codecs
import sys
import re

import omdbapi
import fanarttv

from config import Config

def reconstruct_title(t):
    result = t
    pattern = re.compile(ur'(?P<title>^.*)(?P<prefix>,\s\w+$)', re.U)
    match = re.search(pattern, t)

    if (match is not None):
        prefix = match.group('prefix').lstrip(', ')
        title = match.group('title')

        result = u''+ prefix + ' ' + title

    print u'Reconstructed title: {}'.format(result)
    return result

def movie_meta(dirname):
    pattern = re.compile(ur'(?P<title>^.*)\s\((?P<year>\d{4})\)', re.U)
    match = re.search(pattern, dirname)
    match.groups()

    title = match.group('title')
    year = match.group('year')
    
    movie = omdbapi.search(title=reconstruct_title(title), type='movie')
    print u'Found movie id: {}'.format(movie.get('imdbID'))

    return dict(dirname=dirname, year=year, title=title, imdbid=movie.get('imdbID'))

def scan_music(target):
    pass

def scan_movies(target):
    meta = movie_meta(target)
    fanart = fanarttv.movie_id(meta.get('imdbid'))
    return 

def scan_tv(target):
    pass

def scan_media(target):
  print u'Scanning {}'.format(target)
  dirlist = [d for d in os.listdir(target) if os.path.isdir(os.path.join(target, d))]
  return dirlist
  

if __name__ == "__main__":
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)

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
        scanner(d)
