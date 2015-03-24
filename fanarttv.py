# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
import os
import collections

api_key = u'ca3ec88f4dfce52bf2e86c00fdedf4ff'
url = u'http://webservice.fanart.tv/v3'

# use the proxied url to live inspect reqs in the documentation
url_proxy = u'http://private-anon-9363a01f2-fanarttv.apiary-proxy.com'

movie_mappings = {
    'poster.jpg': 'movieposter', 
    'fanart.jpg': 'moviebackground', 
    'clearart.png': 'hdmovieclearart', #['hdmovieclearart', 'movieart'],
    'logo.png': 'hdmovielogo', #['hdmovielogo', 'movielogo'],
    'disc.png': 'moviedisc',
    'banner.jpg': 'moviebanner',
    'landscape.jpg': 'moviethumb',
    'extrafanart': 'moviebackground'
}

tv_mappings = {
    'poster.jpg': 'tvposter', 
    'season{}.jpg': 'seasonposter',
    'fanart.jpg': 'showbackground', 
    'clearart.png': 'hdclearart', #['hdclearart', 'clearart']
    'character.png': 'characterart',
    'logo.png': 'hdtvlogo',  #['hdtvlogo','clearlogo']
    'banner.jpg': 'tvbanner', 
    'landscape.jpg': 'tvthumb',
    'season{}-landscape.jpg': 'seasonthumb',
    'seasonall-landscape.jpg': 'tvthumb',
    'seasonbanner{}.jpg': 'seasonbanner',
    'extrafanart': 'showbackground',
    'extrathumbs': 'tvthumb'
}

artist_mappings = {
    'logo.png':  'hdmusiclogo', #['hdmusiclogo', 'musiclogo']
    'fanart.jpg': 'artistbackground',
    'banner.jpg': 'musicbanner',
    'folder.jpg': 'artistthumb',
    'extrafanart': 'artistbackground',
    'extrathumbs': 'artistthumb'
}

album_mappings = {
    'folder.jpg': 'albumcover',
    'cdart.png': 'cdart'
}

def get(ident, category=''):
    result = {}
    data = dict(api_key=api_key)

    req = urllib.urlencode(data)
    fullurl = url + u'/' + category + u'/' + ident + u'?' + req

    try:
        #print fullurl
        resp = urllib2.urlopen(fullurl)
    except urllib2.URLError, e:
        result['status'] = 'error'
        return result
    else:
        result = resp.read()

    return json.loads(result)


def movie_art(meta):
    """
    Movies:
        Poster (poster.jpg)
        FanArt (fanart.jpg)
        Extra fanart: extrafanart/(<image ID from provider>.jpg)
        Extrathumbs: extrathumbs/(thumb1.jpg to thumb4.jpg)
        Clearart (clearart.png)
        Logo (logo.png)
        Discart (disc.png)
        Wide Banner Icons (banner.jpg)
        Thumb 16:9 (landscape.jpg) 
    """

    artwork = ['poster.jpg', 'fanart.jpg', 'clearart.png', \
            'logo.png', 'disc.png', 'banner.jpg', 'landscape.jpg',\
            'extrafanart', 'extrathumbs']

    queue = []

    if (meta.get('imdbid') is None):
      print u'No id for meta: {}'.format(meta.get('dirname'))
      return queue

    fanart = get(meta.get('imdbid'), category='movies')

    for art in artwork:
        rpath = movie_mappings.get(art)
        for item in fanart.get(rpath, []):
          if art.startswith('extra'):
            path = os.path.join(meta.get('path'), meta.get('dirname'), art)
            if not os.path.exists(path):
              os.makedirs(path)
            filename = item.get('url').split('/')[-1]
            queue.append((os.path.join(path, filename), item.get('url')))

          else:
            path = os.path.join(meta.get('path'), meta.get('dirname'), art)
            queue.append((path, item.get('url')))
            break

    return queue

def tv_art(meta):
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
    artwork = ['poster.jpg', 'season{}.jpg', 'fanart.jpg', 'clearart.png',\
            'character.png', 'logo.png', 'banner.jpg', 'seasonbanner{}.jpg',\
            'landscape.jpg', 'season{}-landscape.jpg',\
            'seasonall-landscape.jpg', 'extrafanart']

    queue = []

    if (meta.get('tvdbid') is None):
      print u'No id for meta: {}'.format(meta.get('dirname'))
      return queue

    fanart = get(meta.get('tvdbid'), category='tv')

    for art in artwork:
        rpath = tv_mappings.get(art)
        for item in fanart.get(rpath, []):
          if art.startswith('season') and not art.startswith('seasonall'):
            season = os.path.join(meta.get('path'), meta.get('dirname'), \
                art.format(item.get('season')))
            queue.append((season, item.get('url')))
          elif art.startswith('extra'):
            path = os.path.join(meta.get('path'), meta.get('dirname'), art)
            if not os.path.exists(path):
              os.makedirs(path)
            filename = item.get('url').split('/')[-1]
            queue.append((os.path.join(path, filename), item.get('url')))
          else:
            path = os.path.join(meta.get('path'), meta.get('dirname'), art)
            queue.append((path, item.get('url')))
            break

    return queue

def music_art(meta):
    artist_artwork = ['logo.png', 'fanart.jpg', 'banner.jpg', 'folder.jpg',\
        'extrafanart', 'extrathumbs']

    album_artwork = ['folder.jpg', 'cdart.png']

    queue = []

    artist = meta.get('artist')
    if (artist.get('mbid') is None):
      print u'No id for meta: {}'.format(meta.get('dirname'))
      return queue

    fanart = get(artist.get('mbid'), category='music')

    for art in artist_artwork:
        rpath = artist_mappings.get(art)
        for item in fanart.get(rpath, []):
          if art.startswith('extra'):
            path = os.path.join(meta.get('path'), meta.get('dirname'), art)
            if not os.path.exists(path):
              os.makedirs(path)
            filename = item.get('url').split('/')[-1]
            queue.append((os.path.join(path, filename), item.get('url')))
          else:
            path = os.path.join(meta.get('path'), meta.get('dirname'), art)
            queue.append((path, item.get('url')))

    for album in meta.get('albums'):
      albumart = get(album.get('mbid'), category='music/albums')

      if albumart.get('status') is not None:
        print u'Snag hit on album: {}\t({})'.format(album.get('dirname'), album.get('mbid'))
        continue

      for art in album_artwork:
        rpath = album_mappings.get(art)

        albums = albumart.get('albums')
        current = albums.get(album.get('mbid'))
        item = current.get(rpath)

        if item is None:
          continue

        path = os.path.join(meta.get('path'), meta.get('dirname'), album.get('dirname'), art)
        queue.append((path, item[0].get('url')))

    return queue
