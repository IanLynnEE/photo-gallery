# -*- coding: utf-8 -*-
# To make sure {subdir}-001 exit, and all files will be indexed to minimum.
# Do not use os.rename(), so users can think twice.

import os

def is_numeric_string(string):
    try:
        int(string)
    except ValueError:
        return False
    return True

sh = open('rename.sh', 'w')
sh.write('#!/bin/sh\nset -e\n\n')

for sd in os.listdir():
    if not os.path.isdir(sd):
        continue
    if not is_numeric_string(sd):
        continue
    # Get name list of images.
    names = sorted(os.listdir(sd))
    for name in names:
        if '.gif' in name or '.mp4' in name or '.DS_Store' in name:
            names.remove(name)
    # Check if need to sort
    need_to_sort = False
    for i in range(1, len(names)+1):
        if not os.path.isfile(f'{sd}/{sd}-{i:05d}.jpg'):
            if not os.path.isfile(f'{sd}/{sd}-{i:05d}.png'):
                need_to_sort = True
                break

    if need_to_sort:
        # mv to temp name
        for name in names:
            sh.write(f'mv -vn {sd}/{name} {sd}/temp-{name}\n')
        # mv back to currect order 
        for i, name in enumerate(names):
            if 'jpg' in name or 'JPG' in name:
                sh.write(f'mv -vn {sd}/temp-{name} {sd}/{sd}-{i+1:05d}.jpg\n')
            elif 'png' in name or 'PNG' in name:
                sh.write(f'mv -vn {sd}/temp-{name} {sd}/{sd}-{i+1:05d}.png\n')
        sh.write('\n')
        
sh.close()
