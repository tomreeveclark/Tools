# -*- coding: utf-8 -*-
"""

TIMESHEET APP

Created on Tue Aug 23 09:12:08 2016

@author: Tom-R.Clark
"""

import time, datetime, sys

date_today=datetime.datetime.now().strftime('%d_%m_%Y')

def write_file(times):
    
    text_file = open('{0}.txt'.format(date_today), 'w')

    text_file.write('Timesheet Logging for {0}'.format(datetime.datetime.now().strftime('%d:%m:%Y')))
    text_file.write('\n\nProjects worked on:')
    for item in times:
        text_file.write('\nProject: {0}, started at {1}, duration: {2}'.format(item[0], item[1], str(item[2])[:4]))
    text_file.write('\n\nTiming finished at {0}'.format(datetime.datetime.now().strftime('%H:%M:%S')))
    text_file.close()

input('TIMESHEET APP - Press Enter to begin')
print('Timesheet app started at {0}'.format(datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')))

timestamps=[]

project=''
start_time=''
finish_time=''

first_time=True

try:
    while True:
        if first_time==True:
            project=input('\nType a project to start timing, or press Ctrl-C to quit: ')
            start_time = datetime.datetime.now()
            print('Timing {0}, time started: {1}'.format(project, start_time.strftime('%H:%M:%S')))
            first_time=False
            #print(start_time, finish_time)
        else:
            new_project=input('\nType a project to start timing, or press Ctrl-C to quit: ')
            finish_time=datetime.datetime.now()
            timestamps.append((project, start_time.strftime('%H:%M:%S'), finish_time-start_time))
            project=new_project
            start_time = datetime.datetime.now()
            print('Timing {0}, time started: {1}'.format(project, start_time.strftime('%H:%M:%S')))
            #print(start_time, finish_time)
        
except KeyboardInterrupt:
    finish_time=datetime.datetime.now()
    timestamps.append((project, start_time.strftime('%H:%M:%S'), finish_time-start_time))
    print('\n------------------------------')
    print('Timing finished at {0}'.format(datetime.datetime.now().strftime('%H:%M:%S')))
    print('\nProjects worked on today:')
    for item in timestamps:
        print(' > Project: {0}, started at {1}'.format(item[0], item[1]))
    print('\nFile {0} written.'.format(datetime.datetime.now().strftime('%d_%m_%Y.txt')))
    print('------------------------------')
    write_file(timestamps)
    sys.exit(0)    
      


