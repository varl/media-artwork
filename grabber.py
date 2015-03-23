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

def movie_meta(path, dirname):
    """ Handles names in format '<Title> (<year>)' """
    pattern = re.compile(ur'(?P<title>^.*)\s\((?P<year>\d{4})\)', re.U)
    match = re.search(pattern, dirname)
    match.groups()

    title = match.group('title')
    year = match.group('year')
    
    movie = omdbapi.search(title=reconstruct_title(title), type='movie')
    print u'Found movie id: {}'.format(movie.get('imdbID'))

    return dict(path=path, dirname=dirname, year=year, title=title, imdbid=movie.get('imdbID'))

def scan_music(path, target):
    pass

def scan_movie(path, target):
    meta = movie_meta(path, target)
    fanarttv.movie_art(meta)
    return

def find_local_tv(target):
    """
    TV Shows:
        Poster (poster.jpg)
        Season Posters (seasonx.jpg)
        FanArt (fanart.jpg)
        Extra fanart: extrafanart/(<image ID from provider>.jpg)
        Clearart (clearart.png)
        Characterart (character.png)
        Logo (logo.png)
        Wide Banner Icons (banner.jpg)
        Season Banners (seasonbannerx.jpg)
        Thumb 16:9 (landscape.jpg)
        Season Thumb 16:9 (seasonx-landscape.jpg | seasonall-landscape.jpg)
    """
    pass

def scan_tv(path, target):
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

