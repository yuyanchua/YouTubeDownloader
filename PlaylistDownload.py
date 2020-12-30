from pathlib import Path
import os
from pytube import YouTube, Playlist
import traceback


class PlaylistDownloader(object):

    def __init__(self, link, save_path):
        self.link = link
        self.playlist = Playlist(link)
        if len(self.playlist) <= 0:
            print('invalid playlist link')
            raise Exception
        self.playlist_title = self.playlist.title
        self.video_list = self.playlist.video_urls
        self.save_path = save_path
