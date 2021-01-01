from pathlib import Path
import os
from pytube import YouTube, Playlist, exceptions
from YouTubeDownloader.VideoDownload import VideoDownloader
from YouTubeDownloader.YoutubeHelper import *
import traceback

# can combine download and check invalid

resolution_type = ['1080p', '720p', '480p', '360p', '240p']


class PlaylistDownloader(object):

    def __init__(self, link, save_path):
        self.link = link
        self.playlist = Playlist(link)
        if len(self.playlist) <= 0:
            print('invalid playlist link')
            raise exceptions
        self.playlist_title = self.playlist.title
        # print(self.playlist_title)
        self.check_invalid()
        self.video_list = self.playlist.video_urls
        self.save_path = save_path

        self.is_download_caption = None
        self.caption_code = None
        self.caption_code_pref_list = ['zh-Hans', 'zh-Hant', 'en']

        self.is_highest_res = None
        self.resolution_index = None

    def check_invalid(self):
        print('Checking invalid video ...')
        invalid_list = []
        for i in range(len(self.playlist)):
            # print(f'Checking video {i + 1}')
            try:
                video_url = self.playlist.video_urls[i]
                tube = YouTube(video_url)
                tube.check_availability()
                print(f'{i+1}. {tube.title}')

            except Exception:
                # print('Video invalid')
                invalid_list.append(i)
                continue

        for index in invalid_list:
            del self.playlist.video_urls[index]

    # def print_all_video(self):
    #     print('\n' + self.playlist_title)
    #     # for video in self.playlist.videos:
    #     invalid_list = []
    #     for i in range(len(self.playlist)):
    #         try:
    #             video = self.playlist.videos[i]
    #
    #             print(f'{i+1}. {video.title}')
    #         except exceptions.VideoPrivate:
    #             invalid_list.append(i)
    #             continue
    #
    #     for index in invalid_list:
    #         del self.playlist.videos[index]
    #     del invalid_list

    def select_resolution(self):
        print('\nSelect a specific resolution of video')
        print(f'Default = {resolution_type[0]}')
        for i in range(len(resolution_type)):
            print(f'{i+1}. {resolution_type[i]}')

        sel = input('Input: ').rstrip('\r')
        # res = None
        try:
            index = int(sel) - 1
            if not (0 <= index < len(resolution_type)):
                # res = resolution_type[index]
                index = 0

        except ValueError:
            index = 0
            # res = resolution_type[0]

        self.resolution_index = index
        print(f'Downloading video with {resolution_type[index]}')

    def prompt_set_resolution(self):

        print('\nSelect preference of resolution for the downloaded video')
        print('1. Set Highest Resolution')
        print('2. Set Lowest Resolution')
        print('3. Set Specific Resolution')

        sel = input('Input: [default = 1]').rstrip('\r')
        if sel == '2':
            print('Select download with lowest resolution')
            self.is_highest_res = False
        elif sel == '3':
            print('Select download with specific resolution')
            print('Will download video with a lower on grade of resolution if '
                  'the specific resolution is not available')
            self.is_highest_res = False
            self.select_resolution()

        else:
            print('Select download with highest resolution')
            self.is_highest_res = True

    # Download the first available caption only (default - en)
    def prompt_download_caption(self):
        print('Download caption for all video?')
        self.is_download_caption = None
        while self.is_download_caption is None:
            selection = input('Input: [y/n]')
            if selection.lower() == 'y':
                self.is_download_caption = True
            elif selection.lower() == 'n':
                self.is_download_caption = False
            else:
                self.is_download_caption = None
                continue

        # if self.is_download_caption:
        #     # print select caption prompt
        #     self.caption_code = 'zh-Hans'

    def download_stream(self, download_option):
        if download_option == 'audio':
            output_path = self.save_path['audio']
            for video_stream in self.playlist.videos:
                audio = video_stream.streams.get_audio_only('mp4')
                if not audio:
                    print('Audio not available')
                    return
                audio_title = clear_invalid(audio.title)

                mp4_file = output_path / (audio_title + '.mp4')
                mp3_file = get_file_name(output_path, audio_title, 'mp3')
                print(mp3_file)
                print(f'Downloading {audio_title}.mp4')
                audio.download(output_path=output_path, filename=audio_title)

                convert_to_mp3(mp4_file=mp4_file, mp3_file=mp3_file)
            prompt_open_file_location(save_path=output_path)

        elif download_option == 'video':
            self.prompt_set_resolution()
            self.prompt_download_caption()
            output_path = self.save_path['video']

            for video in self.playlist.videos:
                video_stream = video.streams.filter(only_video=True, subtype='mp4')\
                    .order_by('resolution').desc()
                audio_stream = video.streams.get_audio_only('mp4')

                video_title = clear_invalid(video.title)
                video_file = f'video_{video_title}'
                audio_file = f'audio_{video_title}'

                # caption
                # caption = None

                if video.captions:
                    for code in self.caption_code_pref_list:
                        try:
                            caption = video.captions[code]

                            title = video.title
                            if caption:
                                caption.download(title=title, output_path=output_path)
                                break
                        except KeyError:
                            # print(f'{code} not available')
                            continue

                # resolution
                stream = None
                if self.is_highest_res:
                    stream = video_stream.first()
                elif self.is_highest_res is False:
                    if self.resolution_index:
                        res = resolution_type[self.resolution_index]
                        count = 0
                        while not video:
                            query = video_stream.filter(resolution=res)

                            # if preference res not available
                            if len(query) <= 0:
                                print('Specific resolution not available')
                                count += 1
                                res = resolution_type[self.resolution_index + count]
                                continue
                            else:
                                stream = query.first()
                                break

                    else:
                        stream = video_stream.last()

                if stream:
                    print(f'Downloading {video_file} ...')
                    stream.download(output_path=output_path, filename=video_file)

                    print(f'Downloading {audio_file} ...')
                    audio_stream.download(output_path=output_path, filename=audio_file)

                    output_name = get_file_name(output_path, video_title, '.mp4')

                    combine_audio_video(output_path / (video_file + '.mp4'),
                                        output_path / (audio_file + '.mp4'),
                                        'copy',
                                        output_name)

            prompt_open_file_location(output_path)
