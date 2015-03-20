from fanarttv import FanartTv

from socket import gethostname

class Config(object):

  def __init__(self):
    self.categories = ['music', 'tv', 'movies']

    self.paths = {
        'music': u'tmp/music',
        'tv': u'tmp/tv',
        'movies': u'tmp/movies'
    }

  def services(self):
    fanart = FanartTv()
