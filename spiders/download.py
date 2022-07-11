# -*- coding: utf-8 -*-

import os
import subprocess

import requests
from bs4 import BeautifulSoup

cached_images = {}


def get_cached_images_map(url: str) -> dict:
    caches_path = r'/Users/ian/Library/Containers/com.apple.Safari/Data/'\
            r'Library/Caches/com.apple.Safari/WebKitCache'
    seach_text = f'href="{url}"'
    target = subprocess.run(['grep', '-rnwl', caches_path, '-e', seach_text],
                            capture_output=True, text=True)
    path = target.stdout.split('\n')[0].split('/')
    path.pop()
    path = '/'.join(path)
    for file in os.listdir(path):
        if '-blob' in file:
            continue
        with open(os.path.join(path, file), 'r', encoding='latin1') as f:
            head = f.read()
            url = head.split('ÿ')[0].split('\x01')[-1]
            cached_images[url] = os.path.join(path, file) + '-blob'
    return cached_images


def single_image(url: str, folder: str, ID: str, NO: int) -> bool:
    form = url.split('.')[-1]
    name = f'{folder}/{ID}-{NO:05d}.{form}'
    if url in cached_images:
        subprocess.run(['cp', cached_images[url], name])
        print(f'{NO:3d}: {url}')
        return True
    try:
        img = requests.get(url)
        with open(name, 'wb') as f:
            f.write(img.content)
        print(f'{NO:3d}: {url}')
        return True
    except requests.exceptions.RequestException:
        print('Fail:', url)
        return False
    return False


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
