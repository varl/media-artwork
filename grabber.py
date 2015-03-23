# -*- coding: utf-8 -*-
import os
import os.path
import codecs
import sys
import re
import urllib

import omdbapi
import fanarttv
import thetvdb

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

    return dict(path=path, dirname=dirname, year=year, title=title, \
            imdbid=movie.get('imdbID'))

def tv_meta(path, dirname):
    """ This just assumes the folder is the title :> """
    pattern = re.compile(ur'^[^\(]+', re.U)
    match = re.search(pattern, dirname)

    title = match.group().strip()
    print u'Using fixed title: {}'.format(title)

    omdb_series = omdbapi.search(title)
    omdb_imdbid = omdb_series.get('imdbID')
    print u'Found series IMDB id: {}'.format(omdb_imdbid)

    tvdb_series = thetvdb.remote_id(omdb_imdbid)
    print u'Got TVDB result: {}'.format(tvdb_series is not None)

    tvdb_imdbid = tvdb_series[0].find('IMDB_ID').text
    tvdb_id = tvdb_series[0].find('id').text

    print u'Found series TVDB id: {}'.format(tvdb_id)

    if tvdb_imdbid != omdb_imdbid:
        print u'The imdb ids do not match: Name{}, OMDB: {}, TVDB {}'\
                .format(title, omdb_imdbid, tvdb_imdbid)

    return dict(path=path, dirname=dirname, title=dirname, \
            imdb_id=omdb_imdbid, tvdb_id=tvdb_id)

def scan_music(path, target):
    pass

def scan_movie(path, target):
    pass
    #meta = movie_meta(path, target)
    #data = fanarttv.movie_art(meta)
    #return download(data)

def scan_tv(path, target):
    meta = tv_meta(path, target)
    data = fanarttv.tv_art(meta)
    return download(data)

def scan_media(target):
  print u'Scanning {}'.format(target)
  dirlist = [d for d in os.listdir(target) if os.path.isdir(os.path.join(target, d))]
  return dirlist

def download(data):
    for local, remote in data.iteritems():
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

