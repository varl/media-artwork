from fanarttv import FanartTv

class Config(object):

  def __init__(self):

    self.paths = {
      'music': '/media/music',
      'tv': '/media/tv-series',
      'movies': '/media/movies'
    }

  def categories(self):
    return self.paths

  def services(self):
    fanart = FanartTv(self.api_keys.get('fanart.tv'))
