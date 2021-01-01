from YouTubeDownloader.VideoDownload import VideoDownloader
from YouTubeDownloader.PlaylistDownload import PlaylistDownloader
from pathlib import Path
import os
import sys
import traceback
from pytube import exceptions

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
    print(f'\nYouTube Downloader v {0.2}')


def menu():
    print('\nMenu')
    print('1. Download video by url')
    print('2. Download video by playlist')
    print(''.ljust(50, '-'))
    print('x. Exit Program')
    # sel = 0
    sel = input('\nInput: ').rstrip('\r')
    # print(f'\nInput: {2}')
    sel = '2'
    return sel


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
            itag, stream_type = vd.print_stream(queries)

        if itag == 'x':
            print('Cancel download')
            return

        if stream_type == 'video':
            is_download_caption = vd.prompt_caption()

            if is_download_caption:
                caption_index = vd.get_caption_index()
                vd.download_caption(caption_index)

        # caption_code = None
        # while download_caption:
        #     caption_code = vd.print_caption()
        #     if caption_code == 'x':
        #         print('Cancel download caption')
        #         break
        #     elif caption_code is None:
        #         continue
        #     else:
        #         vd.download_caption(caption_code)
        #         break

        vd.download_video(stream_queries=queries, itag=itag)

    except exceptions.VideoUnavailable:
        print('Video is not available or not exist')
        traceback.print_exc()
        return
    except exceptions.RegexMatchError:
        print('Invalid link')
        traceback.print_exc()
        return

    except exceptions:
        print('Pytube encountered error')
        traceback.print_exc()
        return

    except Exception:
        print('Encounter unexpected error')
        traceback.print_exc()
        return


def prompt_playlist_download():
    while True:
        print('\nDownload Option:')
        print('1. Download all in video')
        print('2. Donwload all in audio')
        print(''.ljust(30, '-'))
        print('x. Cancel Download')

        sel = input('Input: ').rstrip('\r')

        print(f'Input: {sel}')
        if sel.lower() == 'x':
            print('Cancel Download')
            return None
        elif sel == '1' or sel == '2':
            return sel
        else:
            continue


def menu_download_by_playlist():
    print('Youtube Playlist Link')
    link = input('Input: ').rstrip('\r')

    try:
        pd = PlaylistDownloader(link, save_path)
        # pd.print_all_video()
        sel = prompt_playlist_download()
        if sel == '1':
            print('Download all video')
            pd.download_stream('video')
            # pd.download_all_video()
        elif sel == '2':
            print('Download all audio')
            pd.download_stream('audio')
            # pd.download_all_audio()

    except:
        traceback.print_exc()


def main():
    # setup folder
    setup()
    header()
    # while True:
    selection = menu()
    # print(selection)

    if selection == '1':
        # print('Select download by url')
        menu_download_by_url()
        # get link
    elif selection == '2':
        # print('Not implemented')
        menu_download_by_playlist()
    elif selection == 'x' or selection == 'X':
        print('Exiting program')
        sys.exit(0)
    else:
        print('Invalid input')


if __name__ == '__main__':
    print('Startup')
    input('Press any key to start').rstrip('\r')

    main()
