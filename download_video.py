from pathlib import Path
from pytube import YouTube
import traceback

SAVE_PATH = Path.cwd()

link = 'https://www.youtube.com/watch?v=te_nocX0gi4'

size_prefix = ['bytes', 'KB', 'MB']


def convert_byte(size):
    div = 0
    while size > 1024:
        size = size / 1024
        div += 1
    return f'{size:.3f} {size_prefix[div]}'


def print_query(queries):
    video_query = queries.filter(only_video=True, subtype='mp4')
    audio_query = queries.get_audio_only('mp4')

    index = 1
    PADDING = 30
    print("Downloading " + queries.first().title + '...')
    print('Video'.center(54, ' '))
    print('|' + 'Number'.center(10, ' ') + "|" +
          'Resolution'.center(20, ' ') + '|' +
          'FileSize'.center(20, ' ') + '|')
    print('|' + ''.ljust(10, '-') + '|' + ''.ljust(20, '-') + '|' + ''.ljust(20, '-') + '|')
    for query in video_query:
        if query.type == 'audio':
            continue

        print('|' + str(index).center(10, ' ') + '|' +
              f'{query.resolution}(.mp4)'.center(20, ' ') + '|' +
              convert_byte(query.filesize+audio_query.filesize).center(20, ' ') + '|')
        index += 1

    print(''.ljust(54, '-'))
    print('Audio'.center(54, ' '))
    print('|' + 'Number'.center(10, ' ') + '|' +
          'Filetype'.center(20, ' ') + '|' +
          'FileSize'.center(20, ' ') + '|')
    print('|' + ''.ljust(10, '-') + '|' + ''.ljust(20, '-') + '|' + ''.ljust(20, '-') + '|')

    print('|' + str(index).center(10, ' ') + '|' +
          f'.mp3({audio_query.abr})'.center(20, ' ') + '|' +
          convert_byte(audio_query.filesize).center(20, ' ') + '|')

    sel = int(input('Select: ').rstrip('\r'))

    if sel == index:
        itag = audio_query.itag
    else:
        query = video_query[sel - 1]
        itag = query.itag

    return itag


try:
    tube = YouTube(link)

    tube.check_availability()

    streamQuery = tube.streams

    # stream = streamQuery.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream = streamQuery.filter(progressive=False, file_extension='mp4')
    stream_itag = print_query(stream)

    stream_query = stream.get_by_itag(stream_itag)
    stream_query.download(output_path=SAVE_PATH)
    # stream.download(output_path=SAVE_PATH)
    # stream.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
except:
    traceback.print_exc()
