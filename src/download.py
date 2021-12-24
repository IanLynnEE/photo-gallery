# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup

def single_image(url, name):
    try:
        img = requests.get(url)
        with open(name, 'wb') as f:
            f.write(img.content)
        print('Done:', url)
        return True
    except:
        print('Fail:', url)
        return False
    return False

def taobao_image(url, ID, NO):
    form = url.split('.')[-1]
    name = f'{ID}-{NO:05d}.{form}'
    try:
        img = requests.get(url)
        with open(name, 'wb') as f:
            f.write(img.content)
        print(f'{NO:4d} {url}')
        return True
    except:
        print('Fail:', url)
        return False
    return False

def taobao_video(soup, ID):
    video = soup.find('video')
    if video == None:
        print('No Video Found!')
    else:
        video_url = video.get('src')
        if video_url == None:
            video = soup.find('source')
            video_url = video.get('src')
        if video_url[0] == '/':
            video_url = 'https:' + video_url 
        cmd = f'ffmpeg -i "{video_url}" {ID}.mp4'
        os.system(cmd)
        print('Vid:', video_url)

def taobao_thumbnail(bar, ID):
    i = 1 
    for img in bar.find_all('img'):
        img_src = img.get('src').split('.jpg')[0]
        img_src = img_src + '.jpg'
        if img_src[0] == '/':
            img_src = 'https:' + img_src
        taobao_image(img_src, ID, i) 
        i += 1
    return i

