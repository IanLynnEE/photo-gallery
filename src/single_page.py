# -*- coding: utf-8 -*-
# Download images in a web page, and save them to static/{website} directory.
# Need a download history file: static/{website}.txt.

import requests
from bs4 import BeautifulSoup

import download


def dropship(root_url: str) -> None:
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
        img_url = 'https:' + img.get('data-src').split('?')[0]
        download.single_image(img_url, 'static/dropship', i, j)
    return


def kiskissing(root_url: str) -> None:
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
        download.single_image(img_url, 'static/kiskissing', i, j)
    return


def lspace(root_url: str) -> None:
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
        download.single_image(img_url, 'static/lspace', i, j)
    return
