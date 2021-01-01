import os
import subprocess


def combine_audio_video(video, audio, codec, output):
    subprocess.run(f'./bin/ffmpeg -i "{video}" -i "{audio}" -c {codec} "{output}"')

    os.remove(video)
    os.remove(audio)


def convert_to_mp3(mp4_file, mp3_file):
    print('Converting to mp3')
    subprocess.run(f'./bin/ffmpeg -i "{mp4_file}" "{mp3_file}"')
    os.remove(mp4_file)


def get_file_name(file_path, file_name, file_type):
    index = 1
    output_name = file_path / f'{file_name}.{file_type}'
    while os.path.exists(output_name):
        output_name = file_path / f'{file_name}_{index}.{file_type}'
        index += 1

    return output_name


def convert_byte(size):
    size_prefix = ['Bytes', 'KB', 'MB', 'GB']
    div = 0
    while size > 1024:
        size = size / 1024
        div += 1
    return f'{size:.3f} {size_prefix[div]}'


def clear_invalid(title):
    invalid_char = ['/', '\\', ':', '?', '*', '"',
                    '|', '<', '>', '#', '.', ',',
                    '$', '\'', '~']
    for char in invalid_char:
        title = title.replace(char, '')

    return title


def prompt_open_file_location(save_path):
    print('Do you want to open the file location?')
    key = input('Enter: [y/n]').rstrip('\r')
    if key.lower() == 'y':
        print(f'Opening {save_path} ...')
        subprocess.run(f'explorer {save_path}')