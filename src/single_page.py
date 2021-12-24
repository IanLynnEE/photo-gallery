# -*- coding: utf-8 -*-
# Download images in a web page, 
# and save them to static/{website} directory.
# Need a download history file: static/{website}.txt.

import requests
from bs4 import BeautifulSoup

import download

def dropship(root_url):
    with open('static/dropship.txt', 'r') as f:   # a+ fail.
        links = f.read().split()
    i = len(links)
    if root_url in links:
        input('Already saved! Press any key to download again.')
    with open('static/dropship.txt', 'a') as f:
        f.write(root_url + '\n')
    res = requests.get(root_url)
    soup = BeautifulSoup(res.text, 'lxml')
    div = soup.find('div', class_='viewimg_list')
    for j, img in enumerate(div.find_all('img')):
        img_url = 'https:' + img.get('src').split('?')[0] 
        name = f'static/dropship/dropship-{i:03d}{j:02d}.jpg'
        download.single_image(img_url, name)
    return

def kiskissing(root_url):
    with open('static/kiskissing.txt', 'r') as f:
        links = f.read().split()
    i = len(links)
    if root_url in links:
        input('Already saved! Press any key to download again.')
    with open('static/kiskissing.txt', 'a') as f:
        f.write(root_url + '\n')
    res = requests.get(root_url)
    soup = BeautifulSoup(res.text, 'lxml')
    div = soup.find('div', class_='MagicToolboxSelectorsContainer')
    for j, img in enumerate(div.find_all('a')):
        img_url = img.get('href')
        name = f'static/kiskissing/kiskissing-{i:03d}{j:02d}.jpg'
        download.single_image(img_url, name)
    return

def lspace(root_url):
    with open('static/lspace.txt', 'r') as f:
        links = f.read().split()
    i = len(links)
    if root_url in links:
        input('Already saved! Press any key to download again.')
    with open('static/lspace.txt', 'a') as f: 
        f.write(root_url + '\n') 
    source = requests.get(root_url)
    soup = BeautifulSoup(source.text, 'lxml')
    for j, img in enumerate(soup.find_all('img', class_='w-100')):
        img_url = 'https:' + img.get('src')
        name = f'static/lspace/lspace-{i:03d}{j:02d}.jpg'
        download.single_image(img_url, name)
    return
