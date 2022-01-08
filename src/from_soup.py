# -*- coding: utf-8 -*-
# Analyze HTML, and save images to static/{ID}.

import os

from bs4 import BeautifulSoup

import download

def aliex(url, soup):
    bool_download_video = (input('Download Video? ') == 'y')
    bool_download_content = (input('Download Content? ') == 'y')
    ID = url.split('/')[-1].split('.')[0]
    os.chdir('aliex')
    if os.path.isdir(ID):
        input('Directory existed!')
    else:
        os.mkdir(ID)
    os.chdir(ID)
    
    if bool_download_video:
        download.taobao_video(soup, ID)

    bar = soup.find('ul', class_='images-view-list')
    i = download.taobao_thumbnail(bar, ID)
       
    if bool_download_content:
        content = soup.find('div', class_='product-overview')
        for p in content.find_all('p'):
            for img in p.find_all('img'):
                img_src = img.get('src')
                if img_src == None:
                    continue
                download.single_image(img_src, '.', ID, i) 
                i += 1
    return


def taobao(url, soup):
    bool_download_content = (input('Download Content? ') == 'y')
    ID = url.split('=')[-1]
    os.chdir('taobao')
    if os.path.isdir(ID):
        os.system(f'open {os.getcwd()}/{ID}')
        input('Directory existed!')
    else:
        os.mkdir(ID)
    os.chdir(ID)

    download.taobao_video(soup, ID) 
    bar = soup.find('ul', id='J_UlThumb')
    i = download.taobao_thumbnail(bar, ID)

    if bool_download_content:
        content = soup.find(id='description')
        for img in content.find_all('img'):
            img_src = img.get('src')
            if img_src[0] == '/':
                img_src = 'https:' + img_src
            download.single_image(img_src, '.', ID, i)
            i += 1
    
    review = soup.find(id='review-image-list')
    if review is not None:
        for p in review.find_all('p'):
           img_src = p.get_text().replace('_40x40.jpg', '')
           download.single_image(img_src, '.', ID, i)
           i += 1
    print('Stored in directory:', os.getcwd())
    return

