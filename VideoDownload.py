from pytube import YouTube
from pytube.cli import on_progress
import traceback
from YouTubeDownloader.YoutubeHelper import *
import os
import subprocess


class VideoDownloader(object):

    def __init__(self, link, save_path):
        self.link = link
        self.tube = YouTube(link, on_progress_callback=on_progress)
        self.tube.check_availability()
        self.stream_queries = self.tube.streams
        self.video_title = clear_invalid(self.stream_queries.first().title)
        self.save_path = save_path

    def limit_query(self):
        temp_queries = []
        HIGHEST_RES = 1080

        for query in self.stream_queries:
            if query.resolution:
                res = int(query.resolution[:-1])
                if res > HIGHEST_RES:
                    del query

    def get_itag_by_index(self, index):
        temp_queries = []
        for query in self.stream_queries:
            if query.resolution:
                res = int(query.resolution[:-1])
                if res <= 1080:
                    temp_queries.append(query)

        return temp_queries[index].itag

    def filter_stream(self, file_extension=None, resolution=None, progressive=None):

        if file_extension:
            self.stream_queries = self.stream_queries.filter(file_extension=file_extension)
        if resolution:
            self.stream_queries = self.stream_queries.filter(resolution=resolution)
        if progressive:
            self.stream_queries = self.stream_queries.filter(progressive=progressive)

        return self.stream_queries

    def print_video_info(self):
        print(self.video_title)
        print(self.tube.description)

    def print_stream(self, stream_queries=None):
        if not stream_queries:
            stream_queries = self.stream_queries

        video_query = stream_queries.filter(only_video=True, subtype='mp4')
        audio_query = stream_queries.get_audio_only('mp4')

        index = 1
        print(self.video_title)
        print('Video'.center(76, ' '))
        print('|' + 'Number'.center(10, ' ') + "|" +
              'Resolution'.center(20, ' ') + '|' +
              'Codec'.center(20, ' ') + '|' +
              'FileSize'.center(20, ' ') + '|')
        print('|' + ''.ljust(10, '-') + '|' + ''.ljust(20, '-') +
              '|' + ''.ljust(20, '-') + '|' + ''.ljust(20, '-') + '|')
        for query in video_query:
            if query.type == 'audio':
                continue

            print('|' + str(index).center(10, ' ') + '|' +
                  f'{query.resolution}_{query.fps}fps(.mp4)'.center(20, ' ') + '|' +
                  f'{query.video_codec}'.center(20, ' ') + '|' +
                  convert_byte(query.filesize + audio_query.filesize).center(20, ' ') + '|')
            index += 1

        print(''.ljust(76, '-'))
        print('Audio'.center(76, ' '))
        print('|' + 'Number'.center(10, ' ') + '|' +
              'Filetype'.center(20, ' ') + '|' +
              'Codec'.center(20, ' ') + '|' +
              'FileSize'.center(20, ' ') + '|')
        print('|' + ''.ljust(10, '-') + '|' +
              ''.ljust(20, '-') + '|' +
              ''.ljust(20, '-') + '|' +
              ''.ljust(20, '-') + '|')

        print('|' + str(index).center(10, ' ') + '|' +
              f'.mp3({audio_query.abr})'.center(20, ' ') + '|' +
              f'{audio_query.audio_codec}'.center(20, ' ') + '|' +
              convert_byte(audio_query.filesize).center(20, ' ') + '|')

        print('x to cancel download')
        sel = input('Select [default = 1]: ').rstrip('\r')
        if sel == '':
            sel = '1'
        elif sel.lower() == 'x':
            itag = 'x'
            return itag

        sel = int(sel)
        if sel == index:
            itag = audio_query.itag
            type = 'audio'
        elif 0 < sel < index:
            query = video_query[sel - 1]
            itag = query.itag
            type = 'video'
        else:
            itag = None
            type = None
            print('Invalid input')

        return itag, type

    def prompt_caption(self):
        caption_num = len(self.tube.caption_tracks)
        if caption_num <= 0:
            print('Caption is unavailable')
            return

        sel = input('Download caption? [y/n]? ').rstrip('\r')
        if sel.lower() == 'y':
            return True
        else:
            return False

    def print_caption(self):
        caption_list = self.tube.caption_tracks
        print('Caption'.center(54, ' '))
        print('|' + 'Number'.center(10, ' ') +
              '|' + 'Code'.center(10, ' ') +
              '|' + 'Language'.center(30, ' ') + '|')
        print('|' + ''.ljust(10, '-') +
              '|' + ''.ljust(10, '-') +
              '|' + ''.ljust(30, '-') + '|')

        for i in range(1, len(caption_list)):
            caption = caption_list[i]
            print('|' + f'{i}'.center(10, ' ') +
                  '|' + f'{caption.code}'.center(10, ' ') +
                  '|' + f'{caption.name}'.center(30, ' ') + '|')

        print('x to cancel download caption')
        sel = input('Select (default = 1): ')
        if sel.lower() == 'x':
            return 'x'

        if sel == '':
            sel = 1

        try:
            sel = int(sel)

            if 0 < sel < len(caption_list):
                return caption_list[sel].code
            else:
                return None
        except:
            return None

    def get_caption_index(self):
        caption_index = None
        while True:
            caption_index = self.print_caption()
            if caption_index == 'x':
                print('Cancel download caption')
                break
            elif caption_index is None:
                continue
            else:
                # self.download_caption(caption_code)
                break

        return caption_index

    def download_caption(self, caption_index):
        caption_query = self.tube.captions
        caption = caption_query[caption_index]
        title = self.stream_queries.first().title
        if caption:
            caption.download(title=title, output_path=self.save_path['video'])

    # def print_stream(self, stream_queries=No  ne):
    #     if not stream_queries:
    #         stream_queries = self.stream_queries
    #
    #
    #     for query in stream_queries:
    #         if query.resolution:
    #             res = int(query.resolution[:-1])
    #             if res > 1080:
    #                 continue
    #         print(query)

    def download_audio(self, stream, save_type):
        output_path = self.save_path[save_type]
        mp4_file = output_path / (self.video_title + '.mp4')

        mp3_file = get_file_name(output_path, self.video_title, 'mp3')
        # mp3_file = output_path / (self.video_title + '.mp3')

        # index = 1
        # while os.path.exists(mp3_file):
        #     mp3_file = output_path / (self.video_title + f'_{index}.mp3')
        #     index += 1

        print(f'Downloading {self.video_title}.mp4')
        stream.download(output_path=output_path)

        convert_to_mp3(mp4_file=mp4_file, mp3_file=mp3_file)
        # print('Converting to mp3')
        # subprocess.run(f'./bin/ffmpeg -i "{mp4_file}" "{mp3_file}"')
        # os.remove(mp4_file)

        prompt_open_file_location(output_path)

    def download_video(self, stream_queries, itag=None):
        if stream_queries is None:
            print('Invalid query')

        self.stream_queries = stream_queries

        print(stream_queries.first().default_filename)
        print(stream_queries.first().subtype)
        query_name = self.video_title

        # sort by highest resolution
        # check if the result query is progressive
        # if not then download the query + the audio
        # combine the video and the audio

        # if got index, download the query with the chosen index
        # if not download, the query with the highest resolution
        stream = None
        if itag:
            stream = stream_queries.get_by_itag(itag)
        else:
            sorted_queries = stream_queries.filter(only_video=True, subtype='mp4'). \
                sort_by('resolution').desc()
            for i in range(len(sorted_queries)):
                stream = sorted_queries[i]
                res = int(stream.resolution[:-1])
                if res <= 1080:
                    break

        if stream.type == 'audio':
            self.download_audio(stream=stream, save_type='audio')
        elif stream.type == 'video':

            # print(stream)
            output_path = self.save_path['video']

            video_name = f'video_{query_name}'
            audio_name = f'audio_{query_name}'

            if not stream.is_progressive:
                print(f'Downloading {video_name} ...')
                stream.download(output_path=output_path, filename=video_name)

                print(f'Downloading {audio_name} ...')
                audio_query = stream_queries.filter(type='audio').first()
                audio_query.download(output_path=output_path, filename=audio_name)

                # index = 1
                # output_name = output_path / f'{query_name}.mp4'
                # while os.path.exists(output_name):
                #     output_name = output_path / f'{query_name}_{index}.mp4'
                #     index += 1

                output_name = get_file_name(output_path, query_name, 'mp4')

                combine_audio_video(output_path / (video_name + '.mp4'),
                                    output_path / (audio_name + '.mp4'),
                                    'copy',
                                    output_name)

            else:
                print(f'Downloading {query_name}.mp4')
                stream.download(output_path=output_path, filename=f'{query_name}')

            prompt_open_file_location(save_path=output_path)
