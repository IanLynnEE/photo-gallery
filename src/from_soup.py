# -*- coding: utf-8 -*-
# Analyze HTML, and save images to static/{ID}.

import os

from bs4 import BeautifulSoup

import download

def aliex(url, soup):
    bool_download_video = (input('Download Video? ') == 'y')
    bool_download_content = (input('Download Content? ') == 'y')
    ID = url.split('/')[-1].split('.')[0]
    folder = f'static/aliex/{ID}'
    if not os.path.isdir('static'):
        os.mkdir('static')
    if not os.path.isdir('static/aliex'):
        os.mkdir('static/aliex')
    if os.path.isdir(folder):
        input('Directory existed!')
    else:
        os.mkdir(folder)
    
    if bool_download_video:
        download.taobao_video(soup, folder, ID)

    bar = soup.find('ul', class_='images-view-list')
    i = download.taobao_thumbnail(bar, folder, ID)
       
    if bool_download_content:
        content = soup.find('div', class_='product-overview')
        for p in content.find_all('p'):
            for img in p.find_all('img'):
                img_src = img.get('src')
                if img_src == None:
                    continue
                download.single_image(img_src, folder, ID, i)
                i += 1
    print(f'Stored in directory: static/aliex/{ID}')
    return


def taobao(url, soup):
    bool_download_content = (input('Download Content? ') == 'y')
    ID = url.split('=')[-1]
    folder = f'static/{ID}'
    if not os.path.isdir('static'):
        os.mkdir('static')
    if os.path.isdir(folder):
        os.system(f'open static/{ID}')
        input('Directory existed!')
    else:
        os.mkdir(folder)

    download.taobao_video(soup, folder, ID)
    bar = soup.find('ul', id='J_UlThumb')
    i = download.taobao_thumbnail(bar, folder, ID)

    if bool_download_content:
        content = soup.find(id='description')
        for img in content.find_all('img'):
            img_src = img.get('src')
            if img_src[0] == '/':
                img_src = 'https:' + img_src
            download.single_image(img_src, folder, ID, i)
            i += 1
    print('Stored in directory:', folder)
    
    if not os.path.isdir('static/review'):
        os.mkdir('static/review')
    i = 1
    review = soup.find(id='review-image-list')
    if review is not None:
        for p in review.find_all('p'):
           img_src = p.get_text().replace('_40x40.jpg', '')
           download.single_image(img_src, 'static/review', ID, i)
           i += 1
    print('Stored in directory: static/review')
    return

