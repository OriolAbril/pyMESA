import numpy as np
from itertools import izip_longest

def terminal_print(iterable, sort=True, order='descending'):
    # the options for the descending parameter are descending or right.
    # it sets the first order direction to the selected one
    if sort:
        iterable=sorted(iterable)
    col_len=len(iterable)/4+1
    if order=='descending':
        for name1,name2,name3,name4 in izip_longest(iterable[:col_len], iterable[col_len:2*col_len], 
                                                    iterable[2*col_len:3*col_len], iterable[3*col_len:], 
                                                    fillvalue=''):
            print '{:<30}{:<30}{:<30}{:<}'.format(name1,name2,name3,name4)
        #first descending and then to the right order
    if order=='right':
        for name1,name2,name3,name4 in izip_longest(iterable[::4], iterable[1::4], 
                                                    iterable[2::4], iterable[3::4], 
                                                    fillvalue=''):
        #first to the right then descending order
            print '{:<30}{:<30}{:<30}{:<}'.format(name1,name2,name3,name4)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i+1
