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

mappings = {
    'poster.jpg': 'movieposter', 
    'fanart.jpg': 'moviebackground', 
    'clearart.png': 'hdmovieclearart', #['hdmovieclearart', 'movieart'],
    'logo.png': 'hdmovielogo', #['hdmovielogo', 'movielogo'],
    'disc.png': 'moviedisc',
    'banner.jpg': 'moviebanner',
    'landscape.jpg': 'moviethumb'
}

def download(data):
    for local, remote in data.iteritems():
        print u'Downloading {} to {}'.format(remote, local)
        filename, headers = urllib.urlretrieve(remote, local)
        print filename
        print headers

def movie_id(mid):
    if mid is None:
        return {}

    data = dict(api_key=api_key)

    req = urllib.urlencode(data)
    fullurl = url + u'/movies/' + mid + u'?' + req
    resp = urllib2.urlopen(fullurl).read()
    return json.loads(resp)

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
            'logo.png', 'disc.png', 'banner.jpg', 'landscape.jpg']

    extra = ['extrafanarts', 'extrathumbs']

    local = {}

    fanart = movie_id(meta.get('imdbid'))

    for art in artwork:
        path = os.path.join(meta.get('path'), meta.get('dirname'), art)

        rpath = mappings.get(art)

        art_list = fanart.get(rpath)

        if isinstance(art_list, collections.MutableSequence):
            for item in art_list:
                local[path] = item.get('url')


    download(local)
    return
