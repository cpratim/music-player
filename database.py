import json
from random import choice

CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-'

_id = lambda length: ''.join(choice(list(CHARSET)) for i in range(length))

def read_data(f):
    with open(f, 'r') as df:
        return json.loads(df.read())

def dump_data(f, d):
    with open(f, 'w') as df:
        json.dump(d, df, indent=4)

class Database(object):

    def __init__(self, file):
        self.file = file

    def add_song(self, title, artist, album, album_art, length):
        data = read_data(self.file)
        file = '-'.join(title.split(' '))
        loc = f'music/{file}.mp3'
        data[title] = {'title': title, 'artist': artist, 'album': album, 'album-art': album_art, 'length': length, 'file': loc}
        dump_data(self.file, data)

    def get_songs(self):
        data = read_data(self.file)
        return data
