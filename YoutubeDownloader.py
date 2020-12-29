from YouTubeDownloader.VideoDownload import VideoDownloader
from pathlib import Path
import os
import sys
import traceback

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
    # else:
    #     print('Directory created')

    if not os.path.isdir(audio_output_path):
        os.makedirs(audio_output_path)
        print(f'Create directory {audio_output_path}')
    # else:
    #     print('Directory created')


def header():
    print(f'YouTube Downloader v {0.1}')


def menu():
    print('Menu')
    print('1. Download video by url')
    print('2. Download video by playlist')
    print(''.ljust(50, '-'))
    print('x. Exit Program')
    # sel = 0
    sel = input('Input: ').rstrip('\r')
    # sel = '1'
    return sel


def prompt_caption():
    sel = input('Download caption? [y/n]? ').rstrip('\r')
    if sel.lower() == 'y':
        return True
    else:
        return False


def menu_download_by_url():
    print('Youtube link')
    link = input("Input: ").rstrip('\r')
    try:
        vd = VideoDownloader(link, save_path)
        queries = vd.filter_stream(file_extension='mp4')
        # itag = vd.print_stream(queries)

        # sel = input("Input: ").rstrip('\r')
        # itag = vd.get_itag_by_index(int(sel)-1)
        itag = None
        while not itag:
            itag = vd.print_stream(queries)

        if itag == 'x':
            print('Cancel download')
            return

        download_caption = prompt_caption()
        caption_code = None
        while download_caption:
            caption_code = vd.print_caption()
            if caption_code == 'x':
                print('Cancel download caption')
                break
            elif caption_code is None:
                continue
            else:
                vd.download_caption(caption_code)
                break

        vd.download_video(stream_queries=queries, itag=itag)

    except:
        print('Invalid link')
        traceback.print_exc()
        return
        # pass


def main():
    # setup folder
    setup()
    header()
    while True:
        selection = menu()
        # print(selection)

        if selection == '1':
            # print('Select download by url')
            menu_download_by_url()
            # get link
        elif selection == '2':
            print('Not implemented')
        elif selection == 'x' or selection == 'X':
            print('Exiting program')
            sys.exit(0)
        else:
            print('Invalid input')


if __name__ == '__main__':
    main()
