# -*- coding: utf-8 -*-
# Check filename extension for all files in all directories under static.

import os

if os.path.isfile('check_type_temp.txt'):
    os.remove('check_type_temp.txt')

for subdir in os.listdir('static'):
    if os.path.isdir(subdir):
        os.system(f'file --mime {subdir}/* >> check_type_temp.txt')

with open('./check_type_temp.txt') as f:
    rows = f.read().split('\n')

for row in rows:
    try:
        name = row.split('.')[0]
        current = row.split(':')[0].split('.')[-1]
        suggest = row.split(';')[0].split('/')[-1]
        if suggest == 'jpeg':
            suggest = 'jpg'
        if current != suggest:
            print(f'mv -vn {name}.{current} {name}.{suggest}\n')
    except IndexError:
        print('# Error!', row)

