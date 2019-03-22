import os

root_dir = '/media/DATA/gringet/lyrica/www.metallyrica.com/lyrica'
first_line = 123
except_count = 0
n_files = 0
song = 0
# Walk in root folder
for root, dirs, files in os.walk(root_dir):
    # For each file
    for name in files:
        # Verify if html
        if name.endswith('.html'):
            file_path = os.path.join(root, name)
            # Read file
            with open(file_path, 'r', errors='replace') as f:
                print(file_path)
                # Go to first lyrics line
                for i in range(first_line):
                    _ = f.readline()
                # Read first line an verify if songs exists
                line = f.readline()
                if not line.endswith('</CENTER>\n'):
                    line = line.split('>')[-1]
                    # Verify if song is not garbage
                    if not line.count('&') + line.count(';') >= 2:
                        print('BEGINNING OF SONG\n')
                        print(line)
                        song = song + 1
                        # Read song
                        while(True):
                            line = f.readline()
                            # verify end of songs
                            if line.endswith('</CENTER>\n'):
                                line = line.split('>')[1]
                                print(line[:-3] + '\n END OF SONGS')
                                break
                            # verify new song
                            elif line.count('<br>') > 1:
                                line = line.split('>')
                                print(line[1][:-3])
                                print('NEW SONG')
                                print(line[-1])
                            # simple song line
                            else:
                                line = line.split('>')[1]
                                print(line)
                            # Cut to text
                            # line = line.split('>')[-1]
print(song)

