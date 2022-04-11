# Simple script that writes all files in cwd to a csv

import os
import csv
import time

cwd = os.getcwd()

files = []

for f in os.listdir():
    print('here!')
    if os.path.isfile(f):
        print('here')
        files.append([f,os.path.getsize(f),time.ctime(os.path.getmtime(f))])

print(files)


with open(os.path.join(cwd,'filelist.csv'),'w', newline='') as fout:
    writer = csv.writer(fout)
    for file in files:
        if not file[0] == 'getFileList.py':
            writer.writerow(file)
