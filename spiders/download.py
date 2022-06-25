# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup


def single_image(url: str, folder: str, ID: str, NO: int) -> bool:
    form = url.split('.')[-1]
    name = f'{folder}/{ID}-{NO:05d}.{form}'
    try:
        img = requests.get(url)
        with open(name, 'wb') as f:
            f.write(img.content)
        print(f'{NO:3d}: {url}')
        return True
    except:
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
    cmd = f'ffmpeg -i "{video_url}" {folder}/{ID}.mp4'
    os.system(cmd)
    print('Vid:', video_url)
    return True


def taobao_thumbnail(bar: BeautifulSoup, folder: str, ID: str) -> int:
    for i, img in enumerate(bar.find_all('img')):
        img_src = img.get('src').split('.jpg')[0] + '.jpg'
        if img_src[0] == '/':
            img_src = 'https:' + img_src
        single_image(img_src, folder, ID, i)
    return i
