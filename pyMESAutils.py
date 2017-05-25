import numpy as np
from itertools import izip_longest
import re

abunPat = re.compile(r'([a-z]{1,3})[0-9]{1,3}$',re.IGNORECASE)
elements=['neut', 'h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p',
        's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga',
        'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd',
        'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'pr', 'nd', 'pm',
        'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w', 're', 'os',
        'ir', 'pt', 'au', 'hg', 'tl', 'pb', 'bi', 'po', 'at', 'rn', 'fr', 'ra', 'ac', 'th', 'pa',
        'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'rf', 'db', 'sg',
        'bh', 'hs', 'mt', 'ds', 'rg', 'uub', 'uut', 'uuq', 'uup', 'uuh', 'uus', 'uuo']

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

def checkElement(el):
    if el in elements:
        return True
    else:
        return False

def getIsos(checklist):
    isos_list = []
    for data_name in checklist:
        abunMatch = abunPat.match(data_name)
        if abunMatch:
            elem_name = abunMatch.groups(1)[0]
            if checkElement(elem_name):
                isos_list.append(data_name)
    return isos_list
