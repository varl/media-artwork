# -*- coding: utf-8 -*-
import os
import os.path
import codecs
import sys

from config import Config

def scan_media(target):
  print 'Scanning %s' % target
  dirlist = [d for d in os.listdir(target) if os.path.isdir(os.path.join(target, d))]
  return dirlist
  

if __name__ == "__main__":
  UTF8Writer = codecs.getwriter('utf8')
  sys.stdout = UTF8Writer(sys.stdout)

  cfg = Config()
  paths = cfg.paths
  media = {}
        
  for category in cfg.categories:
    dirs = scan_media(paths.get(category))
    media[category] = dirs

  print media
