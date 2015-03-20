import urllib
import urllib2
import json
import re

"""
    t = title
    i = id
    type = movie,series,episode
    plot = short,full
    r = xml,json
    tomatoes = true,false
"""
url = 'http://www.omdbapi.com/?'

def search(title='', imdbid='', type='', plot='short', r='json', tomatoes='true'):
    data = dict(t=title.encode('utf-8'), i=imdbid, type=type, plot=plot, r=r, tomatoes=tomatoes)

    req = urllib.urlencode(data)
    resp = urllib2.urlopen(url+req).read()
    return json.loads(resp)
