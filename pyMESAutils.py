import numpy as np
from itertools import izip_longest

def terminal_print(iterable, sort=True, order='descending', columns=4):
    # the options for the descending parameter are descending or right.
    # it sets the first order direction to the selected one
    # the number of columns can only be 4,5
    if sort:
        iterable=sorted(iterable)
    col_len=len(iterable)/columns*np.arange(1,columns)
    for i in range(len(iterable)%columns):
        col_len[i:]+=1
    print len(iterable)
    print col_len
    if columns==4:
        if order=='descending':
            for name1,name2,name3,name4 in izip_longest(iterable[:col_len[0]],
                    iterable[col_len[0]:col_len[1]], iterable[col_len[1]:col_len[2]],
                    iterable[col_len[2]:], fillvalue=''):
                #first descending and then to the right order
                print '{:<30}{:<30}{:<30}{:<}'.format(name1,name2,name3,name4)
        if order=='right':
            for name1,name2,name3,name4 in izip_longest(iterable[::4], iterable[1::4], 
                                                        iterable[2::4], iterable[3::4], 
                                                        fillvalue=''):
                #first to the right then descending order
                print '{:<30}{:<30}{:<30}{:<}'.format(name1,name2,name3,name4)
    if columns==5:
        if order=='descending':
            for name1,name2,name3,name4,name5 in izip_longest(iterable[:col_len[0]],
                    iterable[col_len[0]:col_len[1]], iterable[col_len[1]:col_len[2]],
                    iterable[col_len[2]:col_len[3]], iterable[col_len[3]:], 
                    fillvalue=''):
                #first descending and then to the right order
                print '{:<25}{:<25}{:<25}{:<25}{:<}'.format(name1,name2,name3,name4,name5)
        if order=='right':
            for name1,name2,name3,name4,name5 in izip_longest(iterable[::5], iterable[1::5], 
                                                              iterable[2::5], iterable[3::5], 
                                                              iterable[4::5], fillvalue=''):
                #first to the right then descending order
                print '{:<25}{:<25}{:<25}{:<25}{:<}'.format(name1,name2,name3,name4,name5)


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i+1
