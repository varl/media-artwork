#!/usr/bin/bash

MOVIES_DIR="movies"
MUSIC_DIR="music"
TV_DIR="tv"

pushd ..

echo $(pwd)

if [ ! -d "$MOVIES_DIR" ]; then
  echo "Creating $MOVIES_DIR"
  mkdir "$MOVIES_DIR"
fi
if [ ! -d "$TV_DIR" ]; then
  echo "Creating $TV_DIR"
  mkdir "$TV_DIR"
fi
if [ ! -d "$MUSIC_DIR" ]; then
  echo "Creating $MUSIC_DIR"
  mkdir "$MUSIC_DIR"
fi

pushd "$MOVIES_DIR"
xargs -0 mkdir -p < ../testdata/movies_structure.txt
popd

pushd "$TV_DIR"
xargs -0 mkdir -p < ../testdata/tv_structure.txt
popd

pushd "$MUSIC_DIR"
xargs -0 mkdir -p < ../testdata/music_structure.txt
popd
