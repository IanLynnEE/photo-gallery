# -*- coding: utf-8 -*-
# Download all images from certain website,
# and save them to static/{website} directory.
# Will try to read download history from static/{website}.txt.

import time
import requests
from bs4 import BeautifulSoup

from src import download


support_websites = ['bananamoon', 'billabong', 'bowermillet']


def match(url: str) -> bool:
    if 'bananamoon' in url:
        bananamoon(url)
    elif 'billabong' in url:
        billabong(url)
    elif 'bowermillet' in url:
        bowermillet(url)
    else:
        return False
    return True


def bananamoon(root_url: str) -> None:
    with open('static/bananamoon.txt', 'r') as f:
        links = f.read().split()
    start = len(links)
    res = requests.get(root_url)
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.find_all('a', class_='product-item-link'):
        link = item.get('href')
        if link not in links:
            links.append(link)
    for i in range(start, len(links), 1):
        res = requests.get(links[i])
        soup = BeautifulSoup(res.text, 'lxml')
        print('\nIn', links[i])
        for j, img in enumerate(soup.find_all('img', class_='gallery-image')):
            img_url = img.get('data-src')
            download.single_image(img_url, 'static/bananamoon', i, j)
        time.sleep(5)
    with open('static/bananamoon.txt', 'w') as f:
        for link in links:
            f.write(link + '\n')
    return


def billabong(root_url: str) -> None:
    with open('static/billabong.txt', 'r') as f:
        links = f.read().split()
    start = len(links)
    res = requests.get(root_url)
    soup = BeautifulSoup(res.text, 'lxml')
    for item in soup.find_all('div', class_='name'):
        link = item.find('a').get('href')
        if link not in links:
            links.append(link)
    for i in range(start, len(links), 1):
        res = requests.get(links[i])
        soup = BeautifulSoup(res.text, 'lxml')
        div = soup.find('div', class_='productthumbnails')
        print('\nIn', links[i])
        j = 1
        for j, img in enumerate(div.find_all('img')):
            # Very low risk of img.get('src') is None.
            img_url = img.get('src').replace('large', 'hi-res')
            download.single_image(img_url, 'static/billabong', i, j)
        time.sleep(5)
    with open('static/billabong.txt', 'w') as f:
        for link in links:
            f.write(link + '\n')
    return


def bowermillet(root_url: str) -> None:
    with open('static/bowermillet.txt', 'r') as f:
        links = f.read().split()
    start = len(links)
    res = requests.get(root_url)
    soup = BeautifulSoup(res.text, 'lxml')
    for div in soup.find_all('div', class_='product-thumb'):
        link = div.find('a').get('href')
        if link not in links:
            links.append(link)
    for i in range(start, len(links), 1):
        res = requests.get(links[i])
        soup = BeautifulSoup(res.text, 'lxml')
        div = soup.find('div', class_='swiper-wrapper')
        print('\nIn', links[i])
        for j, img in enumerate(div.find_all('a')):
            img_url = img.get('href')
            download.single_image(img_url, 'static/bowermillet', i, j)
        time.sleep(5)
    with open('static/bowermillet.txt', 'w') as f:
        for link in links:
            f.write(link + '\n')
    return
