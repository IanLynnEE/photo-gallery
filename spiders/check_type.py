# -*- coding: utf-8 -*-
# Check filename extension for all files under `static`.

import os
import subprocess


def check_type(path: str) -> None:
    for root, dirs, files in os.walk(path):
        mine_list = subprocess.run(
            f'file --mime-type {root}/*',
            shell=True,
            capture_output=True,
            text=True
        ).stdout.strip().split('\n')

        for mine in mine_list:
            if (cmd := generate_mv_cmd(mine=mine)) is not None:
                print(cmd)


def generate_mv_cmd(*, mine: str = None, filename: str = None) -> None | str:
    """Return a command to rename a file with correct extension if needed.

    Args:
        mine (str)(optional): The output of `file --mime-type <filename>`.
        filename (str)(optional): The filename to run `file` command.

    Returns:
        None | str: A command to rename the file if needed.
    """
    if mine is None and filename is None:
        raise ValueError('At least one argument is required.')
    if mine is None:
        mine = subprocess.run(
            ['file', '--mime-type', filename],
            capture_output=True,
            text=True
        ).stdout.strip()
    try:
        filename = mine.split(':')[0]
        media_type = mine.split(':')[1].split('/')[0].strip()
        filename, current = os.path.splitext(filename)
        suggest = '.' + mine.split(':')[1].split('/')[1]

        if media_type != 'image':
            return
        if is_same_extension(current, suggest):
            return
        return f'mv -vn {filename}{current} {filename}{suggest}'
    except IndexError:
        return '# ' + mine


def is_same_extension(a: str, b: str) -> bool:
    a, b = a.lower(), b.lower()
    if a == b:
        return True
    if a == '.jpeg' and b == '.jpg':
        return True
    if a == '.jpg' and b == '.jpeg':
        return True
    return False


if __name__ == '__main__':
    check_type('static')
