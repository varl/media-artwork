# -*- coding: utf-8 -*-
from config import Config

def scan_media(target):
  print 'Scanning %s (%s)' % target

if __name__ == "__main__":
  cfg = Config()
  
  for category, path in cfg.categories().iteritems():
    cat = category, path
    scan_media(cat)
