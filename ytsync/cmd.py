from __future__ import unicode_literals
import youtube_dl

import logging
import logging.handlers
import os
import re


YTSYNC_DIR = ".ytsync"
CONFIG_FILE = "playlists"
LOG_FILE = "ytsync-log"

logger = logging.getLogger(__name__)
logger.addHandler(logging.handlers.RotatingFileHandler(os.path.join(YTSYNC_DIR, LOG_FILE), backupCount=5, maxBytes=100000))
logger.setLevel(logging.INFO)


def main():
    """
    Download new files from all playlists.

    We perform a diff against existing files based on the contents of the playlist. This isn't strictly necessary
    because the downloader won't download files that are already present in the target directory, but I want to
    avoid scraping pages if possible, for fear of rate-limiting.
    """
    top_dir = os.getcwd()
    playlists = open(os.path.join(YTSYNC_DIR, CONFIG_FILE)).readlines()
    info_fetcher = youtube_dl.YoutubeDL({'skip_download': True, 'extract_flat': 'in_playlist'})
    downloader = youtube_dl.YoutubeDL({'ignoreerrors': True})
    for playlist in playlists:
        logger.info("Processing playlist {}".format(playlist))
        # Get videos in playlist so we can diff
        try:
            info = info_fetcher.extract_info(playlist, download=False)
        except Exception as e:
            logger.error("Error fetching info for {}".format(playlist))
            logger.exception(e)
        playlist_title = info['title']
        playlist_dir = re.sub(r'\W+', '_', playlist_title)
        if not os.path.exists(playlist_dir):
            os.mkdir(playlist_dir)
            logger.info("Created {}".format(playlist_dir))
        # diff
        existing = set()
        for filename in os.listdir(playlist_dir):
            try:
                name = filename.rsplit('.', 1)[0]
            except:
                continue
            existing.add(name)
        to_download = set()
        for entry in info['entries']:
            name = info_fetcher.prepare_filename(entry).rsplit('.', 1)[0]
            if name not in existing:
                to_download.add(entry['url'])
                logger.info("{} added to download list".format(entry['url']))
        # download
        os.chdir(playlist_dir)
        if to_download:
            try:
                downloader.download(list(to_download))
            except Exception as e:
                logger.error("Error downloading new videos for playlist {}".format(playlist_title))
                logger.exception(e)
        else:
            logger.info("{} had no new entries.".format(playlist_title))
        os.chdir(top_dir)

if __name__ == '__main__':
    main()
