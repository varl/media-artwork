import urllib
import urllib2
import json

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
    data = dict(title=title.encode('utf-8'), imdbid=imdbid, type=type, plot=plot, r=r, tomatoes=tomatoes)

    req = urllib.urlencode(data)
    print req
    #resp = urllib2.urlopen(url).read()
    #return json.loads(resp)

