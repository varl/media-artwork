# -*- coding: utf-8 -*-
class FanartTv(object):

  def __init__(self):
    self.api_key = 'ca3ec88f4dfce52bf2e86c00fdedf4ff'
    self.url = 'http://webservice.fanart.tv/v3'
    self.categories = ['movies', 'tv', 'music']

    # use the proxied url to live inspect reqs in the documentation
    self.url_proxy = 'http://private-anon-9363a01f2-fanarttv.apiary-proxy.com'

  def search(self, term):
    pass
