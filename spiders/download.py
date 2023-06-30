# -*- coding: utf-8 -*-

import os
import subprocess

import requests
from bs4 import BeautifulSoup

from .check_type import generate_mv_cmd

cached_images = {}


def search_caches(url: str) -> bool:
    """Search in the cache of Safari and find the cached images.

    Args:
        url (str): url of an image or a webpage.

    Returns:
        bool: True if cache hit.
    """
    global cached_images

    cache_hit = False
    if url in cached_images:
        return True

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
            cache_hit = True
            cached_images[img_url] = filename + '-blob'
    return cache_hit


def single_image(url: str, folder: str, ID: str, NO: int) -> bool:
    global cached_images

    form = url.split('.')[-1]
    name = os.path.join(folder, f'{ID}-{NO:05d}.{form}')

    try:
        if search_caches(url):
            subprocess.run(['cp', cached_images[url], name])
            print(f'{NO:3d}: (cached) {url}')
        else:
            img = requests.get(url)
            with open(name, 'wb') as f:
                f.write(img.content)
            print(f'{NO:3d}: {url}')
    except requests.exceptions.RequestException:
        print('Fail:', url)
        return False

    if (cmd := generate_mv_cmd(filename=name)) is not None:
        subprocess.run(cmd, shell=True)
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
        img_src = img.get('src').split('.jpg')[0] + '.jpg'
        if img_src[0] == '/':
            img_src = 'https:' + img_src
        single_image(img_src, folder, ID, i)
    return i
