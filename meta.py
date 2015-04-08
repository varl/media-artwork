#-*- coding: utf-8 -*-
import os
import os.path
import re

import omdbapi
import thetvdb
import musicbrainz

def music_meta(path, dirname):
  print

  albums = []
  dirnames = scan_media(os.path.join(path, dirname))
  for album in dirnames:
    pattern = re.compile(ur'(?P<title>^.*)\s\[(?P<year>\d{4})\]', re.U)
    match = re.search(pattern, album)

    if match is None:
      continue

    title = match.group('title')
    year = match.group('year')
    
    release_group = musicbrainz.search_releasegroup(title, year, dirname, album)

    if release_group is not None:
      albums.append(release_group)

  artist = musicbrainz.search_artist(dirname, albums)
  
  return dict(path=path, dirname=dirname, artist=artist, albums=albums)

def movie_meta(path, dirname):
    print 
    """ Handles names in format '<Title> (<year>)' """
    pattern = re.compile(ur'(?P<title>^.*)\s\((?P<year>\d{4})\)', re.U)
    match = re.search(pattern, dirname)

    title = match.group('title')
    year = match.group('year')
    
    new_title = reconstruct_title(title)
    movie = omdbapi.search(title=new_title, year=year, type='movie')

    if movie.get('Response') == u'False':
      print 'Retrying without unicode chars ({})'.format(new_title.encode('ascii', 'ignore'))
      movie = omdbapi.search(title=new_title.encode('ascii', 'ignore'),\
          type='movie')
      
    print u'Found movie id: {}'.format(movie.get('imdbID'))

    return dict(path=path, dirname=dirname, year=year, title=title, \
            imdbid=movie.get('imdbID'))

def tv_meta(path, dirname):
    print
    """ This just assumes the folder is the title :> """
    pattern = re.compile(ur'^[^\(]+', re.U)
    match = re.search(pattern, dirname)

    title = match.group().strip()
    print u'Using fixed title: {}'.format(title)

    omdb_series = omdbapi.search(title)
    omdb_imdbid = omdb_series.get('imdbID')
    print u'Found series IMDB id: {}'.format(omdb_imdbid)

    tvdb_series = thetvdb.remote_id(omdb_imdbid)
    print u'Got TVDB result: {}'.format(len(tvdb_series))

    tvdb_imdbid = ''
    tvdbid = ''

    if len(tvdb_series) != 0:
      tvdb_imdbid = tvdb_series[0].find('IMDB_ID').text
      tvdbid = tvdb_series[0].find('id').text

    print u'Found series TVDB id: {}'.format(tvdbid)

    if tvdb_imdbid != omdb_imdbid:
      print u'The imdb ids do not match: Name: {}, OMDB: {}, TVDB: {}'\
                .format(title, omdb_imdbid, tvdb_imdbid)

    return dict(path=path, dirname=dirname, title=dirname, \
            imdbid=omdb_imdbid, tvdbid=tvdbid)

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

def scan_media(target):
  if not os.path.isdir(target):
    print u'Path does not exist, skipping {}'.format(target)
    return []

  print u'Scanning {}'.format(target)
  dirlist = [d for d in os.listdir(target) if os.path.isdir(os.path.join(target, d))]
  return dirlist

