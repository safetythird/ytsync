# ytsync

A little command line utility to keep Youtube audio playlists synced to your computer using [youtube-dl](https://github.com/rg3/youtube-dl).

Example usage:

```
  cd my_music_dir
  mkdir .ytsync
  echo http://my_playlist_url > .ytsync/playlists
  echo http://my_other_playlist_url >> .ytsync/playlists
  ytsync
```
This will download the files from both of your playlists as audio files into subdirectories in the current directory, each named after its respective playlist.
