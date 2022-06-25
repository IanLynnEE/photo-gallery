# -*- coding: utf-8 -*-
# Download images in a web page, and save them to static/{website} directory.
# Need a download history file: static/{website}.txt.

import requests
from bs4 import BeautifulSoup

from . import download


support_websites = ['dropship', 'lspace', 'myroxyfoxy', 'zabota', 'smolensk']


def match(url: str) -> bool:
    if 'dropship' in url:
        dropship(url)
    elif 'lspace' in url:
        lspace(url)
    elif 'myroxyfoxy' in url:
        myroxyfoxy(url)
    elif 'zabota' in url:
        zabota(url)
    elif '80ajegaffddjnjizgfue' in url:
        smolensk(url)
    else:
        return False
    return True


def _check_history(website: str, url: str) -> int:
    with open(f'static/{website}.txt', 'r') as f:
        downloaded_links = f.read().split()
    if url in downloaded_links:
        input('Already saved! Press ENTER to download again.')
    with open(f'static/{website}.txt', 'a') as f:
        f.write(url + '\n')
    return len(downloaded_links)


def dropship(root_url: str) -> None:
    i = _check_history('dropship', root_url)
    res = requests.get(root_url)
    soup = BeautifulSoup(res.text, 'lxml')
    div = soup.find('div', class_='viewimg_list')
    for j, img in enumerate(div.find_all('img')):
        img_url = 'https:' + img.get('data-src').split('?')[0]
        download.single_image(img_url, 'static/dropship', i, j)
    return


def lspace(root_url: str) -> None:
    i = _check_history('lspace', root_url)
    source = requests.get(root_url)
    soup = BeautifulSoup(source.text, 'lxml')
    div = soup.find('div', class_='gallery-thumbs')
    for j, img in enumerate(div.find_all('img', class_='w-100')):
        img_url = 'https:' + img.get('src').replace('_600x@2x.progressive', '')
        download.single_image(img_url, 'static/lspace', i, j)
    return


def myroxyfoxy(url: str) -> None:
    i = _check_history('myroxyfoxy', url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    for j, img in enumerate(soup.find_all('img', class_='cnt_item')):
        img_url = 'https://myroxyfoxy.ru' + img.get('src')
        download.single_image(img_url, 'static/myroxyfoxy', i, j)
    return


def zabota(url: str) -> None:
    i = _check_history('zabota', url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    for j, img in enumerate(soup.find_all('a', class_='thumblisticon')):
        img_url = img.get('href')
        download.single_image(img_url, 'static/zabota', i, j)
    return


def smolensk(url: str) -> None:
    i = _check_history('smolensk', url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    div = soup.find('div', class_='detail_big_pic')
    for j, img in enumerate(div.find_all('a')):
        img_url = 'https://xn--80ajegaffddjnjizgfue.xn--p1ai' + img.get('href')
        download.single_image(img_url, 'static/smolensk', i, j)
    return
