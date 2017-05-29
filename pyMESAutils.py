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
    # the number of columns can only be 1,4,5
    if sort:
        iterable=sorted(iterable)
    col_len=len(iterable)/columns*np.arange(1,columns)
    for i in range(len(iterable)%columns):
        col_len[i:]+=1
    if columns==1:
        for name in iterable:
            print name
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

def getExtremes(data,rng=50,maximums=True,minimums=True):
    length=len(data)
    k=rng*1
    maxims=[]
    minims=[]
    for point in xrange(rng, length-rng):
        entornind=range(k-rng, k)+range(k+1, k+rng+1)
        entorn=data[entornind]
        value=data[k]
        if maximums:
            if value>np.max(entorn):
                maxims.append(k)
        if minimums:
            if value<np.min(entorn):
                minims.append(k)
        k+=1
    return maxims, minims
def readProfileFast(name): # created from nugridpy function _read_mesafile
    f=open(name,'r')
    lines=[f.readline() for line in xrange(6)]
    hval  = lines[2].split()
    hlist = lines[1].split()
    hdr = {}
    for a,b in zip(hlist,hval):
        hdr[a] = float(b)

    cols    = {}
    colname = lines[5].split()
    for b,a in enumerate(colname):
        cols[a] = b

    num_zones=int(hval[hlist.index('num_zones')])
    data = np.empty((num_zones, len(colname)),dtype='float64')
    for i in range(num_zones):
        line = f.readline()
        v=line.split()
        try:
            data[i,:]=np.array(v,dtype='float64')
        except ValueError:
            for item in v:
                if item.__contains__('.') and not item.__contains__('E'):
                    v[v.index(item)]='0'
            data[i,:]=np.array(v,dtype='float64')

    f.close()
    return hdr, cols, data
