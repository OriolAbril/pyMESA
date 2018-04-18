import numpy as np
import pandas as pd
from itertools import zip_longest
import re,os

def read_mesafile(filename,only_hdr=False,**kwargs):
    r'''
    Function to read either history or profile .data files and return 2 
    pandas dataframes, the header and the body data.
    
    Parameters:
    -----------
    
    filename : str
        Name of the file. Can contain the path.
    
    only_hdr : boolean,  default False.
        Return only header data.
    
    kwargs : 
        Keyword argumets passed to pandas.read_csv when
        reading the body data.
    '''
    
    header_attr = pd.read_csv(filename,delim_whitespace=True,skiprows=1,nrows=1)
    if only_hdr:
        return header_attr

    data = pd.read_csv(filename,delim_whitespace=True,skiprows=5,**kwargs)
    
    return header_attr, data

def terminal_print(iterable, sort=True, order='descending', columns='auto'):
    '''
    Print a list organized in columns, following the style of the ls command
    
    Parameters:
    -----------
    iterable : list or tuple
        iterable containing all the elements that have to be printed
    sort : boolean, default True
        sort the elements in iterable
    order : ('descending' | 'right'), default 'descending'
        the options for the descending parameter are descending and right.
        it choses which one is used first
    columns = int or 'auto', default 'auto'
        Number of columns of the printed list, 'auto' sets the number of 
        columns in order to fix their width to the maximum length of the 
        strings in iterable plus 5
    '''
    rows, screenwidth=os.popen('stty size', 'r').read().split()
    screenwidth = int(screenwidth)
    maxwidth=max([len(str(chunk)) for chunk in iterable])
    if columns=='auto':
        columns=screenwidth/(maxwidth+5)
    colwidth=max(maxwidth+1,screenwidth/columns)
    formatlist=['{:<%d}' %colwidth for i in xrange(columns-1)]
    formatlist.append('{:<}')
    formatstr=''.join(formatlist)
    if sort:
        iterable=sorted(iterable)
    if columns==1:
        for name in iterable:
            print(name)
    else:
        if order=='descending':
            col_len=len(iterable)/columns*np.arange(0,columns)
            for i in range(len(iterable)%columns):
                col_len[i:]+=1
            col_len=np.append(col_len,None)
            args=[iterable[col_len[i]:col_len[i+1]] for i in xrange(columns)]
        if order=='right':
            args=[iterable[i::columns] for i in xrange(columns)]
        for name in izip_longest(*args, fillvalue=''):
            print(formatstr.format(*name))

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

