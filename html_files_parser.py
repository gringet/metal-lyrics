import os
from time import time
import re
import html2text

root_dir = '/home/gringet/websites/www.metallyrica.com/lyrica/'
first_line_index = 123
n_song = 0
t0 = time()

def print_song(song):
    global n_song
    n_song += 1
    h = html2text.HTML2Text() 
    sanity_chars = ['[', ']', '(', ')', '\\', '/', ' -', ':', ';', u'\uFFFD']
    sanity_regexs = [
        re.compile(r'\[([\w\d\s]*?)\]'),
        re.compile(r'\(([\w\d\s]*?)\)')
    ]
    # supress [xxxxx] and (xxxxx) strings (e.g. [CHORUS])
    for sanity_regex in sanity_regexs:
        matchs = sanity_regex.findall(song)
        for match in matchs:
            song = song.replace(match, '')
    # supress non wanted characters
    for sanity_char in sanity_chars:
        song = song.replace(sanity_char, '')
    lines = song.split('\n')
    # translate html characters
    for line in lines:
        line = h.handle(line)

# Walk in root folder
for root, dirs, files in os.walk(root_dir):
    # For each file
    for name in files:
        # Verify if html
        if name.endswith('.html'):
            file_path = os.path.join(root, name)
            # Read file
            with open(file_path, 'r', errors='replace') as f:
                is_song = False
                for i, line in enumerate(f):
                    # Go to first lyrics line
                    if i == first_line_index:
                        # BEGINNING OF SONGS
                        if not line.endswith('</CENTER>\n'):
                            is_song = True
                            current_song = line.split('>')[-1]
                    elif is_song:
                        # END OF SONGS
                        if line.endswith('</CENTER>\n'):
                            current_song += line.split('<br>')[0]
                            print_song(current_song)
                            is_song = False
                        # NEW SONG
                        elif line.count('<br>') > 1:
                            # LAST SONG LINE
                            if line.startswith('<br>'):
                                current_song += line.split('<br>')[1]
                            else:
                                current_song += line.split('<br>')[0]
                            print_song(current_song)
                            # FIRST NEW SONG LINE
                            current_song = line.split('>')[-1]
                        # CURRENT SONG LINE
                        else:
                            current_song += line.split('>')[-1]

print('Songs: {}\nTime: {} \nTime per song: {}'.format(n_song, time() - t0, (time() - t0) / n_song))

