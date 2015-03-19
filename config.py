from fanarttv import FanartTv

from socket import gethostname

class Config(object):

  def __init__(self):
    self.categories = ['music', 'tv', 'movies']

    if gethostname() == 'cerebralcortex':
      self.paths = {
        'music': '/media/music',
        'tv': '/media/tv-series',
        'movies': '/media/movies'
      }
    else:
      self.paths = {
        'music': '/cygdrive/z/music',
        'tv': '/cygdrive/z/tv-series',
        'movies': '/cygdrive/z/movies'
      }

  def services(self):
    fanart = FanartTv(self.api_keys.get('fanart.tv'))
