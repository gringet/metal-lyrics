import os

wget --recursive --no-clobber --html-extension --domains metallyrica.com http://www.metallyrica.com/

root_dir = '/home/gringet/websites/www.metallyrica.com/lyrica'
first_line = 123
except_count = 0
n_files = 0
for root, dirs, files in os.walk(root_dir):
    for name in files:
        n_files = n_files + 1
        if name.endswith('.html'):
            with open(os.path.join(root, name), 'r', errors='replace') as f:
                for i, line in enumerate(f):
                    if i == first_line:
                        print(line.split('>')[-1])