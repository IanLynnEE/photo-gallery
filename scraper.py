import src


def main():
    root_url = input('URL: ')
    if src.single_page.match(root_url):
        return
    if src.all_page.match(root_url):
        return
    if src.from_soup.match():
        return
    print('Error! Unsupported website.')


if __name__ == '__main__':
    main()
