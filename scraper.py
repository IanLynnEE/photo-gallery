import spiders


def main():
    root_url = input('URL: ')
    if spiders.single_page.match(root_url):
        return
    if spiders.all_page.match(root_url):
        return
    if spiders.from_soup.match():
        return
    print('Error! Unsupported website.')


if __name__ == '__main__':
    main()
