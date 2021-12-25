# -*- coding: utf-8 -*-
# Check filename extension for all files in all directories under static.

import os

'''
# Not an error free way, but faster
if os.path.isfile('check_type_temp.txt'):
    os.remove('check_type_temp.txt')
for path, subdirs, files in os.walk('static'):
    for folder in subdirs:
        target = os.path.join(path, folder)
        os.system(f'file --mime {target}/* >> check_type_temp.txt')
'''

with open('check_type_temp.txt') as f:
    rows = f.read().split('\n')

for row in rows:
    try:
        name = row.split('.')[0]
        current = row.split(':')[0].split('.')[-1]
        suggest = row.split(';')[0].split('/')[-1]
        if suggest == 'jpeg': 
            suggest = 'jpg'
        if current != suggest and suggest in ['jpg', 'png', 'gif']:
            print(f'mv -vn {name}.{current} {name}.{suggest}')
    except IndexError:
        print('# Error!', row)

