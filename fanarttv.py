# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

api_key = u'ca3ec88f4dfce52bf2e86c00fdedf4ff'
url = u'http://webservice.fanart.tv/v3'

# use the proxied url to live inspect reqs in the documentation
url_proxy = u'http://private-anon-9363a01f2-fanarttv.apiary-proxy.com'

def movie_id(mid):
    if mid is None:
        return None

    data = dict(api_key=api_key)

    req = urllib.urlencode(data)
    fullurl = url + u'/movies/' + mid + u'?' + req
    print fullurl
    resp = urllib2.urlopen(fullurl).read()
    return json.loads(resp)

