import pafy
import vlc
import time
import sys
import os


def print_usage_and_exit():
    print('''Usage:
            - to add a song: t -a youtube_url name
            - to play a song: t name
            - to list all available songs: t -l''')
    exit()


SONGS_FOLDER = 'songs'
END_STATE = 'State.Ended'

sys_args = sys.argv
if sys_args[1] == '-a':
    if len(sys_args) != 4:
        print_usage_and_exit()

    my_url = sys_args[2]
    name = SONGS_FOLDER + '/' + sys_args[3] + '.m4a'

    if not os.path.isdir(SONGS_FOLDER):
        os.mkdir(SONGS_FOLDER)

    print('Downloading...')
    info = pafy.new(my_url)
    audio = info.getbestaudio(preftype='m4a')
    print(name)
    audio.download(filepath=name, remux_audio=True)
    print('Downloaded!')
elif sys_args[1] == '-l':
    songs = os.listdir(SONGS_FOLDER)
    for song in songs:
        print(song.split('.')[0])
else:
    full_name = None
    to_play = sys_args[1]
    songs = os.listdir(SONGS_FOLDER)
    for song in songs:
        song_name = song.split('.')[0]
        if song_name == to_play:
            full_name = SONGS_FOLDER + '/' + song
            break
    if not full_name:
        print_usage_and_exit()

    sound = vlc.MediaPlayer(full_name)

    sound.play()
    while END_STATE not in str(sound.get_state()):
        time.sleep(1)
