import sys
sys.path.append('src')

import single_page
import all_page
import from_soup

url = input('URL: ')

if 'dropship' in url:
    single_page.dropship(url)
elif 'kiskissing' in url:
    single_page.kiskissing(url)
elif 'lspace' in url:
    single_page.lspace(url)

elif 'bananamoon' in url:
    all_page.banana(url)
elif 'billabong' in url:
    all_page.billabong(url)
elif 'bowermillet' in url:
    all_page.bowermillet(url)

else:
    input('Try to analyse HTML from clipboard. Press any key to start...')
    HTML = str(clipboard.paste())
    soup = BeautifulSoup(HTML, 'lxml')
    url = soup.find('link', {'rel': 'canonical'}).get('href')
    if 'aliexpress' in url:     
        from_soup.aliex(url, soup)
    elif 'taobao' in url:      
        from_soup.taobao(url, soup)
    elif 'tmall' in url:       
        from_soup.taobao(url,soup)
    else:
        print('Error! Unsupported website.')
    # Clear clipboard
    # os.system('pbcopy < /dev/null')
