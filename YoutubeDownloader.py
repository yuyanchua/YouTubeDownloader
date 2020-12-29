from YouTubeDownloader.VideoDownload import VideoDownloader
from pathlib import Path
import os
import sys

curr_path = Path.cwd()
video_output_path = curr_path / 'video'
audio_output_path = curr_path / 'audio'
save_path = {
        'video' : video_output_path,
        'audio' : audio_output_path
    }

def setup():
    if not os.path.isdir(video_output_path):
        os.makedirs(video_output_path)
        print(f'Create directory {video_output_path}')
    else:
        print('Directory created')

    if not os.path.isdir(audio_output_path):
        os.makedirs(audio_output_path)
        print(f'Create directory {audio_output_path}')
    else:
        print('Directory created')


def menu():
    print('Menu')
    print('1. Download video by url')
    # sel = 0
    # sel = input('Input: ').rstrip('\r')
    sel = '1'
    return sel


def menu_download_by_url():
    print('Youtube link')
    # link = input("Input: ").rstrip('\r')
    link = 'https://www.youtube.com/watch?v=4b69koOYry4'
    vd = VideoDownloader(link, save_path)
    queries = vd.filter_stream(file_extension='mp4')
    itag = vd.print_stream(queries)

    # sel = input("Input: ").rstrip('\r')
    # itag = vd.get_itag_by_index(int(sel)-1)

    vd.download_video(stream_queries=queries, itag=itag)


def main():
    # setup folder
    setup()

    selection = menu()
    print(selection)

    if selection == '1':
        print('Select download by url')
        menu_download_by_url()
        # get link
    else:
        print('Invalid input')


if __name__ == '__main__':
    main()