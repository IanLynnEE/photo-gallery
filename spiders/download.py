# -*- coding: utf-8 -*-

import os
import subprocess
import time

import requests
from bs4 import BeautifulSoup

from .check_type import generate_mv_cmd

cached_images = {}


def search_caches(url: str) -> None:
    """Search in the cache of Safari and find the cached images.

    Args:
        url (str): url of an image or a webpage.
    """
    global cached_images

    # Use `grep` to search in cache directory.
    caches_path = os.path.join(
        os.path.expanduser('~'),
        'Library/Containers/com.apple.Safari/Data/Library/Caches/',
        'com.apple.Safari/WebKitCache/Version 16/Records'
    )
    target = subprocess.run(
            ['grep', '-rnwl', f'{caches_path}', '-e', f'{url}'],
            capture_output=True,
            text=True
    )

    # Extract the cached images. Filenames ended with '-blob' are images,
    # but we need to find the corresponding img_url by non-blob files.
    for filename in target.stdout.split('\n'):
        if '-blob' in filename or len(filename) == 0:
            continue
        with open(filename, 'r', encoding='latin1') as f:
            head = f.read()
            img_url = head.split('ÿ')[0].split('\x01')[-1]
        if os.path.exists(filename + '-blob'):
            cached_images[img_url] = filename + '-blob'
    return


def single_image(url: str, folder: str, ID: str, NO: int) -> bool:
    global cached_images

    if url.startswith('//'):
        url = 'https:' + url

    form = url.split('.')[-1]
    name = os.path.join(folder, f'{ID}-{NO:05d}.{form}')

    try:
        if url not in cached_images:
            search_caches(os.path.dirname(url))
        if url not in cached_images:
            search_caches(url)
        if url in cached_images:
            subprocess.run(['cp', cached_images[url], name])
            print(f'{NO:3d}: (cached) {url}')
        elif url.endswith('.gif'):
            print(f'{NO:3d}: (ignored) {url}')
        else:
            # Taobao will not allow us to download images directly.
            # Make the user open the image in Safari.
            # Then, user can run the script again to extract images from cache.
            subprocess.run(['open', '-a', 'Safari', url])
            time.sleep(1)
            img = requests.get(url)
            with open(name, 'wb') as f:
                f.write(img.content)
            print(f'{NO:3d}: {url}')
    except requests.exceptions.RequestException:
        print('Fail:', url)
        return False

    if (cmd := generate_mv_cmd(filename=name)) is not None:
        subprocess.run(cmd, shell=True, capture_output=True)
    return True


def wildberries_images(folder: str, serial: str) -> None:
    series = int(serial) // 10000 * 10000
    for j in range(1, 100):
        name = f'{folder}/{serial}-{j}.jpg'
        url = f'https://images.wbstatic.net/big/new/{series}/{serial}-{j}.jpg'
        img = requests.get(url)
        if 'id="sc404"' in img.text:
            break
        with open(name, 'wb') as f:
            f.write(img.content)
        print(url)
    return


def taobao_video(soup: BeautifulSoup, folder: str, ID: str) -> bool:
    video = soup.find('video')
    if video is None:
        print('No Video Found!')
        return False
    video_url = video.get('src')
    if video_url is None:
        video = soup.find('source')
        video_url = video.get('src')
    if video_url[0] == '/':
        video_url = 'https:' + video_url
    subprocess.run(['ffmpeg', '-i', video_url, f'{folder}/{ID}.mp4'])
    print('Vid:', video_url)
    return True


def taobao_thumbnail(bar: BeautifulSoup, folder: str, ID: str) -> int:
    for i, img in enumerate(bar.find_all('img')):
        img_src: str = img.get('src').split('.jpg')[0] + '.jpg'

        # Ruten adds '_m' to the end of the thumbnail url (small image).
        if img_src.endswith('_m.jpg'):
            img_src = img_src[:-6] + '.jpg'
        single_image(img_src, folder, ID, i)
    return i
