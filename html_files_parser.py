import os
from time import time
from random import shuffle
import re
import html2text


class dataset:
    root_dir = ''
    first_line_index = 0
    songs = []
    chars = []
    batch_id = 0
    char_indices = None
    indices_char = None

    def __init__(self, root_dir, first_line_index=123):
        self.root_dir = root_dir
        self.first_line_index = first_line_index
        self.parse_html_songs()
        self.compute_chars()

    def get_batch(self, batch_size):
        if (self.batch_id + 1) * batch_size < len(self.songs): 
            text = ' '.join(
                self.songs[
                    self.batch_id * batch_size:(self.batch_id + 1) * batch_size
                    ]
            )
            return text
        else:
            self.batch_id = 0
            self.shuffle()
            return self.get_batch(batch_size)

    def shuffle(self):
        shuffle(self.songs)


    def compute_chars(self):
        text = ' '.join(self.songs)
        self.chars = sorted(list(set(text)))
        print('Total Number of Unique Characters:', len(self.chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))
        print(self.char_indices)


    def parse_song(self, song):
        h = html2text.HTML2Text() 
        sanity_chars = ['[', ']', '(', ')', '\\', '/', ' -', ':', ';', u'\uFFFD']
        sanity_regexs = [
            re.compile(r'\[([\w\d\s]*?)\]'),
            re.compile(r'\(([\w\d\s]*?)\)')
        ]
        # translate html characters
        song = h.handle(song)
        # supress [xxxxx] and (xxxxx) strings (e.g. [CHORUS])
        for sanity_regex in sanity_regexs:
            matchs = sanity_regex.findall(song)
            for match in matchs:
                song = song.replace(match, '')
        # supress non wanted characters
        for sanity_char in sanity_chars:
            song = song.replace(sanity_char, '')
        song = song.replace('\n', ' ')
        self.songs.append(song)

    def parse_html_songs(self):
        print('Parsing started')
        files_paths = []
        # Walk in root folder
        for root, _, files in os.walk(self.root_dir):
            # For each file
            for name in files:
                # Verify if html
                if name.endswith('.html'):
                    files_paths.append(os.path.join(root, name))
        shuffle(files_paths)
        for file_path in files_paths:
            # Read file
            with open(file_path, 'r', errors='replace') as f:
                is_song = False
                for i, line in enumerate(f):
                    # Go to first lyrics line
                    if i == self.first_line_index:
                        # BEGINNING OF SONGS
                        if not line.endswith('</CENTER>\n'):
                            is_song = True
                            current_song = line.split('>')[-1]
                    elif is_song:
                        # END OF SONGS
                        if line.endswith('</CENTER>\n'):
                            current_song += line.split('<br>')[0]
                            self.parse_song(current_song)
                            is_song = False
                        # NEW SONG
                        elif line.count('<br>') > 1:
                            # LAST SONG LINE
                            if line.startswith('<br>'):
                                current_song += line.split('<br>')[1]
                            else:
                                current_song += line.split('<br>')[0]
                                self.parse_song(current_song)
                                # FIRST NEW SONG LINE
                                current_song = line.split('>')[-1]
                        # CURRENT SONG LINE
                        else:
                            current_song += line.split('>')[-1]
        print('Parsing finished')