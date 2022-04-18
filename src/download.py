# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup

def single_image(url, folder, ID, NO):
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

def taobao_video(soup, folder, ID):
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
        cmd = f'ffmpeg -i "{video_url}" {folder}/{ID}.mp4'
        os.system(cmd)
        print('Vid:', video_url)
    return
    
def taobao_thumbnail(bar, folder, ID):
    i = 1 
    for img in bar.find_all('img'):
        img_src = img.get('src').split('.jpg')[0]
        img_src = img_src + '.jpg'
        if img_src[0] == '/':
            img_src = 'https:' + img_src
        single_image(img_src, folder, ID, i) 
        i += 1
    return i

