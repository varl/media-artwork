media-artwork
=============

## tl;dr

A no frills artwork downloader without dependencies other than python 2.7.

## installation

```
$ git clone git@github.com:varl/media-artwork.git
$ cd media-artwork
$ python2.7 ./grabber.py 2>&1 > ~/media-artwork.log
```

# media archive structure

The program attempts to use as much meta-data from the directory structure as
is possible. Provided in the `tmp/testdata` directory you can find examples on
the structure used. A summary is as follows:

* Movies: `Title (Year)`
* TV Series: `Title/SeasonX`
* Music: `Artist/Album [Year]`

# what does it download?

Artist: 
- FanArt (fanart.jpg)
- Extra fanart: extrafanart/(<image ID from provider.jpg>)
- Logo (logo.png)
- Banner (banner.jpg)
- Artist thumb (folder.jpg)
- Extra thumbs (extrathumbs)

Album:
- Cover (folder.jpg)
- CdART (cdart.png)

TV shows:
- Poster (poster.jpg)
- Season Posters (seasonx.jpg)
- FanArt (fanart.jpg)
- Extra fanart: extrafanart/(<image ID from provider>.jpg)
- Clearart (clearart.png)
- Characterart (character.png)
- Logo (logo.png)
- Wide Banner Icons (banner.jpg)
- Season Banners (seasonbannerx.jpg)
- Thumb 16:9 (landscape.jpg)
- Season Thumb 16:9 (seasonx-landscape.jpg | seasonall-landscape.jpg)

Movies:
- Poster (poster.jpg)
- FanArt (fanart.jpg)
- Extra fanart: extrafanart/(<image ID from provider>.jpg)
- Extrathumbs: extrathumbs/(thumb1.jpg to thumb4.jpg)
- Clearart (clearart.png)
- Logo (logo.png)
- Discart (disc.png)
- Wide Banner Icons (banner.jpg)
- Thumb 16:9 (landscape.jpg)

