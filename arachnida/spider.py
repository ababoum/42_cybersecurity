#!/usr/bin/env python3

import shutil
from bs4 import BeautifulSoup
import requests
import sys


recurvise = False
recursive_depth = 5
downloads_path = 'C:\\Users\\ababo\\OneDrive\\Gestion des finances\\42_work\\42_cybersecurity\\arachnida\\data\\'
initial_url = ''

extensions_allowed = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp'
]

for arg in sys.argv:
    if arg == '-r':
        recurvise = True
    elif arg == '-l':
        try:
            recursive_depth = int(sys.argv[sys.argv.index(arg) + 1])
        except:
            print('Invalid recursive depth. Using default value (5).')
    elif arg == '-p':
        try:
            downloads_path = sys.argv[sys.argv.index(arg) + 1]
        except:
            print('Invalid path. Using default value (./data/).')
    elif sys.argv.index(arg) == len(sys.argv) - 1 and arg != '-r' \
            and arg != '-l' and arg != '-p' and arg != sys.argv[0]:
        initial_url = arg

if initial_url == '':
    print('No URL provided.')
    exit()

if not initial_url.startswith('https'):
    initial_url = 'https://' + initial_url


##########################################################


def get_images(url: str, depth: int):
    response = requests.get(url)
    if (response.status_code != 200):
        print('Error: ' + str(response.status_code))
        exit()
    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.select('img')

    index_url = 'https://' + url.split('/')[2]

    for img in images:
        src = img.get('src')
        if src.startswith('//'):
            src = 'https:' + src
        elif src.startswith('/') and not src.startswith('//'):
            src = index_url + src
        if src.startswith('http'):
            if src.endswith(tuple(extensions_allowed)):
                print(src)
                res = requests.get(src, stream=True)
                if res.status_code == 200:
                    with open(downloads_path + src.split('/')[-1], 'wb') as f:
                        shutil.copyfileobj(res.raw, f)
                else:
                    print(f'Error while loading image {src}: {res.status_code}')

    if recurvise and depth > 0:
        links = soup.select('a')
        for link in links:
            href = link.get('href')
            if href.startswith('/'):
                href = index_url + href
            if href.startswith('http'):
                get_images(href, depth - 1)

##########################################################

get_images(initial_url, recursive_depth)
