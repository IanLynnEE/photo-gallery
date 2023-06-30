# -*- coding: utf-8 -*-
# Analyze HTML, and save images to static/{ID}.

import os

from bs4 import BeautifulSoup
import pyperclip

from . import download


support_websites = ['aliexpress', 'taobao', 'review', 'wildberries']


def match() -> bool:
    input('Try to analyse HTML from clipboard. Press any key to start...')
    HTML = str(pyperclip.paste())
    soup = BeautifulSoup(HTML, 'html.parser')
    try:
        url = soup.find('link', {'rel': 'canonical'}).get('href')
    except AttributeError:
        url = soup.find('base').get('href')
    if 'aliexpress' in url:
        aliexpress(url, soup)
    elif 'taobao' in url:
        taobao(url, soup)
    elif 'tmall' in url:
        taobao(url, soup)
    elif 'wildberries' in url:
        wildberries(soup)
    else:
        return False
    return True


def wildberries(soup: BeautifulSoup) -> None:
    same_series_ul = soup.find_all('ul', class_='swiper-wrapper')[1]
    for link in same_series_ul.find_all('a', class_='img-plug'):
        serial = link.get('href').split('/')[4]
        download.wildberries_images('static/wildberries', serial)
    return


def aliexpress(url: str, soup: BeautifulSoup) -> None:
    bool_download_content = (input('Download Content? ') == 'y')
    ID = url.split('/')[-1].split('.')[0]
    folder = f'static/aliexpress/{ID}'
    if os.path.isdir(folder):
        input('Directory existed!')
    else:
        os.mkdir(folder)

    download.taobao_video(soup, folder, ID)
    bar = soup.find('ul', class_='images-view-list')
    i = download.taobao_thumbnail(bar, folder, ID)

    if bool_download_content:
        content = soup.find('div', class_='product-overview')
        for p in content.find_all('p'):
            for img in p.find_all('img'):
                img_src = img.get('src')
                if img_src is None:
                    continue
                i += 1
                download.single_image(img_src, folder, ID, i)
    print(f'Stored in directory: {folder}')
    return


def taobao(url: str, soup: BeautifulSoup) -> None:
    ID = url.split('=')[-1]
    folder = f'static/taobao/{ID}'
    if os.path.isdir(folder):
        input('Directory existed!')
    else:
        os.mkdir(folder)

    download.taobao_video(soup, folder, ID)
    bar = soup.find('ul', id='J_UlThumb')
    i = download.taobao_thumbnail(bar, folder, ID)

    content = soup.find(id='description')
    for img in content.find_all('img'):
        img_src = img.get('src')
        if img_src[0] == '/':
            img_src = 'https:' + img_src
        i += 1
        download.single_image(img_src, folder, ID, i)
    print('Stored in directory:', folder)

    review = soup.find(id='review-image-list')
    if review is None:
        return
    for i, p in enumerate(review.find_all('p')):
        img_src = p.get_text().replace('_40x40.jpg', '')
        download.single_image(img_src, 'static/review', ID, i)
    print('Stored in directory: static/review')
    return
