import numpy as np
import pandas as pd
from itertools import izip_longest
import re,os

abunPat = re.compile(r'([a-z]{1,3})([0-9]{1,3})$',re.IGNORECASE)
elements=['neut', 'h', 'he', 'li', 'be', 'b', 'c', 'n', 'o', 'f', 'ne', 'na', 'mg', 'al', 'si', 'p',
        's', 'cl', 'ar', 'k', 'ca', 'sc', 'ti', 'v', 'cr', 'mn', 'fe', 'co', 'ni', 'cu', 'zn', 'ga',
        'ge', 'as', 'se', 'br', 'kr', 'rb', 'sr', 'y', 'zr', 'nb', 'mo', 'tc', 'ru', 'rh', 'pd',
        'ag', 'cd', 'in', 'sn', 'sb', 'te', 'i', 'xe', 'cs', 'ba', 'la', 'ce', 'pr', 'nd', 'pm',
        'sm', 'eu', 'gd', 'tb', 'dy', 'ho', 'er', 'tm', 'yb', 'lu', 'hf', 'ta', 'w', 're', 'os',
        'ir', 'pt', 'au', 'hg', 'tl', 'pb', 'bi', 'po', 'at', 'rn', 'fr', 'ra', 'ac', 'th', 'pa',
        'u', 'np', 'pu', 'am', 'cm', 'bk', 'cf', 'es', 'fm', 'md', 'no', 'lr', 'rf', 'db', 'sg',
        'bh', 'hs', 'mt', 'ds', 'rg', 'uub', 'uut', 'uuq', 'uup', 'uuh', 'uus', 'uuo']
#..anders & grevesse 1989 solar mass fractions
sol_comp_ag89 =[ 7.0573E-01, 4.8010E-05, 2.9291E-05, 2.7521E-01, 6.4957E-10, 
        9.3490E-09, 1.6619E-10, 1.0674E-09, 4.7301E-09, 3.0324E-03, 
        3.6501E-05, 1.1049E-03, 4.3634E-06, 9.5918E-03, 3.8873E-06, 
        2.1673E-05, 4.0515E-07, 1.6189E-03, 4.1274E-06, 1.3022E-04, 
        3.3394E-05, 5.1480E-04, 6.7664E-05, 7.7605E-05, 5.8052E-05, 
        6.5301E-04, 3.4257E-05, 2.3524E-05, 8.1551E-06, 3.9581E-04, 
        3.2221E-06, 1.8663E-05, 9.3793E-08, 2.5320E-06, 8.5449E-07, 
        7.7402E-05, 1.5379E-05, 2.6307E-08, 3.4725E-06, 4.4519E-10, 
        2.6342E-07, 5.9898E-05, 4.1964E-07, 8.9734E-07, 1.4135E-06,
        2.7926E-09, 1.3841E-07, 3.8929E-08, 2.2340E-07, 2.0805E-07, 
        2.1491E-06, 1.6361E-07, 1.6442E-07, 9.2579E-10, 3.7669E-07, 
        7.4240E-07, 1.4863E-05, 1.7160E-06, 4.3573E-07, 1.3286E-05, 
        7.1301E-05, 1.1686E-03, 2.8548E-05, 3.6971E-06, 3.3579E-06, 
        4.9441E-05, 1.9578E-05, 8.5944E-07, 2.7759E-06, 7.2687E-07, 
        5.7528E-07, 2.6471E-07, 9.9237E-07, 5.8765E-07, 8.7619E-08, 
        4.0593E-07, 1.3811E-08, 3.9619E-08, 2.7119E-08, 4.3204E-08, 
        5.9372E-08, 1.7136E-08, 8.1237E-08, 1.7840E-08, 1.2445E-08, 
        1.0295E-09, 1.0766E-08, 9.1542E-09, 2.9003E-08, 6.2529E-08, 
        1.1823E-08, 1.1950E-08, 1.2006E-08, 3.0187E-10, 2.0216E-09, 
        1.0682E-08, 1.0833E-08, 5.4607E-08, 1.7055E-08, 1.1008E-08, 
        4.3353E-09, 2.8047E-10, 5.0468E-09, 3.6091E-09, 4.3183E-08, 
        1.0446E-08, 1.3363E-08, 2.9463E-09, 4.5612E-09, 4.7079E-09, 
        7.7706E-10, 1.6420E-09, 8.7966E-10, 5.6114E-10, 9.7562E-10, 
        1.0320E-09, 5.9868E-10, 1.5245E-09, 6.2225E-10, 2.5012E-10, 
        8.6761E-11, 5.9099E-10, 5.9190E-10, 8.0731E-10, 1.5171E-09, 
        9.1547E-10, 8.9625E-10, 3.6637E-11, 4.0775E-10, 8.2335E-10, 
        1.0189E-09, 1.0053E-09, 4.5354E-10, 6.8205E-10, 6.4517E-10, 
        5.3893E-11, 3.9065E-11, 5.5927E-10, 5.7839E-10, 1.0992E-09, 
        5.6309E-10, 1.3351E-09, 3.5504E-10, 2.2581E-11, 5.1197E-10, 
        1.0539E-10, 7.1802E-11, 3.9852E-11, 1.6285E-09, 8.6713E-10, 
        2.7609E-09, 9.8731E-10, 3.7639E-09, 5.4622E-10, 6.9318E-10, 
        5.4174E-10, 4.1069E-10, 1.3052E-11, 3.8266E-10, 1.3316E-10, 
        7.1827E-10, 1.0814E-09, 3.1553E-09, 4.9538E-09, 5.3600E-09, 
        2.8912E-09, 1.7910E-11, 1.6223E-11, 3.3349E-10, 4.1767E-09, 
        6.7411E-10, 3.3799E-09, 4.1403E-09, 1.5558E-09, 1.2832E-09, 
        1.2515E-09, 1.5652E-11, 1.5125E-11, 3.6946E-10, 1.0108E-09, 
        1.2144E-09, 1.7466E-09, 1.1240E-08, 1.3858E-12, 1.5681E-09, 
        7.4306E-12, 9.9136E-12, 3.5767E-09, 4.5258E-10, 5.9562E-10, 
        8.0817E-10, 3.6533E-10, 7.1757E-10, 2.5198E-10, 5.2441E-10, 
        1.7857E-10, 1.7719E-10, 2.9140E-11, 1.4390E-10, 1.0931E-10, 
        1.3417E-10, 7.2470E-11, 2.6491E-10, 2.2827E-10, 1.7761E-10, 
        1.9660E-10, 2.5376E-12, 2.8008E-11, 1.9133E-10, 2.6675E-10, 
        2.0492E-10, 3.2772E-10, 2.9180E-10, 2.8274E-10, 8.6812E-13, 
        1.4787E-12, 3.7315E-11, 3.0340E-10, 4.1387E-10, 4.0489E-10, 
        4.6047E-10, 3.7104E-10, 1.4342E-12, 1.6759E-11, 3.5397E-10,
        2.4332E-10, 2.8557E-10, 1.6082E-10, 1.6159E-10, 1.3599E-12, 
        3.2509E-11, 1.5312E-10, 2.3624E-10, 1.7504E-10, 3.4682E-10, 
        1.4023E-10, 1.5803E-10, 4.2293E-12, 1.0783E-12, 3.4992E-11, 
        1.2581E-10, 1.8550E-10, 9.3272E-11, 2.4131E-10, 1.1292E-14, 
        9.4772E-11, 7.8768E-13, 1.6113E-10, 8.7950E-11, 1.8989E-10, 
        1.7878E-10, 9.0315E-11, 1.5326E-10, 5.6782E-13, 5.0342E-11, 
        5.1086E-11, 4.2704E-10, 5.2110E-10, 8.5547E-10, 1.3453E-09, 
        1.1933E-09, 2.0211E-09, 8.1702E-13, 5.0994E-11, 2.1641E-09, 
        2.2344E-09, 1.6757E-09, 4.8231E-10, 9.3184E-10, 2.3797E-12,
        1.7079E-10, 2.8843E-10, 3.9764E-10, 2.2828E-10, 5.1607E-10, 
        1.2023E-10, 2.7882E-10, 6.7411E-10, 3.1529E-10, 3.1369E-09, 
        3.4034E-09, 9.6809E-09, 7.6127E-10, 1.9659E-10, 3.8519E-13, 
        5.3760E-11]
stable_isos = [ 'h1','h2','he3','he4','li6','li7','be9','b10',
        'b11','c12','c13','n14','n15','o16','o17','o18',
        'f19','ne20','ne21','ne22','na23','mg24','mg25','mg26',
        'al27','si28','si29','si30','p31','s32','s33','s34',
        's36','cl35','cl37','ar36','ar38','ar40','k39','k40',
        'k41','ca40','ca42','ca43','ca44','ca46','ca48','sc45',
        'ti46','ti47','ti48','ti49','ti50','v50','v51','cr50',
        'cr52','cr53','cr54','mn55','fe54','fe56','fe57','fe58',
        'co59','ni58','ni60','ni61','ni62','ni64','cu63','cu65',
        'zn64','zn66','zn67','zn68','zn70','ga69','ga71','ge70',
        'ge72','ge73','ge74','ge76','as75','se74','se76','se77',
        'se78','se80','se82','br79','br81','kr78','kr80','kr82',
        'kr83','kr84','kr86','rb85','rb87','sr84','sr86','sr87',
        'sr88','y89','zr90','zr91','zr92','zr94','zr96','nb93',
        'mo92','mo94','mo95','mo96','mo97','mo98','mo100','ru96',
        'ru98','ru99','ru100','ru101','ru102','ru104','rh103','pd102',
        'pd104','pd105','pd106','pd108','pd110','ag107','ag109','cd106',
        'cd108','cd110','cd111','cd112','cd113','cd114','cd116','in113',
        'in115','sn112','sn114','sn115','sn116','sn117','sn118','sn119',
        'sn120','sn122','sn124','sb121','sb123','te120','te122','te123',
        'te124','te125','te126','te128','te130','i127','xe124','xe126',
        'xe128','xe129','xe130','xe131','xe132','xe134','xe136','cs133',
        'ba130','ba132','ba134','ba135','ba136','ba137','ba138','la138',
        'la139','ce136','ce138','ce140','ce142','pr141','nd142','nd143',
        'nd144','nd145','nd146','nd148','nd150','sm144','sm147','sm148',
        'sm149','sm150','sm152','sm154','eu151','eu153','gd152','gd154',
        'gd155','gd156','gd157','gd158','gd160','tb159','dy156','dy158',
        'dy160','dy161','dy162','dy163','dy164','ho165','er162','er164',
        'er166','er167','er168','er170','tm169','yb168','yb170','yb171',
        'yb172','yb173','yb174','yb176','lu175','lu176','hf174','hf176',
        'hf177','hf178','hf179','hf180','ta180','ta181','w180','w182',
        'w183','w184','w186','re185','re187','os184','os186','os187',
        'os188','os189','os190','os192','ir191','ir193','pt190','pt192',
        'pt194','pt195','pt196','pt198','au197','hg196','hg198','hg199',
        'hg200','hg201','hg202','hg204','tl203','tl205','pb204','pb206',
        'pb207','pb208','bi209','th232','u235','u238']

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
            print name
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
            print formatstr.format(*name)


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
    memory=0
    for point in xrange(rng, length-rng):
        entornind=range(k-rng, k)+range(k+1, k+rng+1)
        entorn=data[entornind]
        value=data[k]
        if maximums:
            if value>np.max(entorn):
                maxims.append(k)
            elif (value>=np.max(entorn) and memory!=value):
                print 'Same maximum value corresponding to a double value'
                maxims.append(k)
                memory=value*1
        if minimums:
            if value<np.min(entorn):
                minims.append(k)
            elif (value<=np.min(entorn) and memory!=value):
                print 'Same minimum value corresponding to a double value'
                minims.append(k)
                memory=value*1
        k+=1
    #print maxims, minims
    return maxims, minims


def getMaxsMins(array,len1,len2,num_bursts=None):
    maxims, minims=getExtremes(array, rng=len1)
    if num_bursts!=None:
        print num_bursts
        if len(maxims)!=num_bursts:
            maxims2, minims2=getExtremes(array, rng=len2)
            if maxims[0]!=maxims2[0]:
                print 'hello max'
                maxims=[maxims2[0]]+maxims
        if len(minims)!=num_bursts:
            maxims2, minims2=getExtremes(array, rng=len2)
            if minims[-1]!=minims2[-1]:
                print 'hello min'
                minims+=[minims2[-1]]
        return maxims,minims
    print maxims,minims
    if len(maxims)==len(minims)-1:
        maxims2, minims2=getExtremes(array, rng=len2)
        try:
            if maxims[-1]!=maxims2[-1]:
                maxims+=[maxims2[-1]]
            else:
                minims=minims[:-1]
        except IndexError:
            minims=minims[:-1]
    if len(maxims)==len(minims)+1:
        maxims2, minims2=getExtremes(array, rng=len2)
        try:
            if minims[-1]!=minims2[-1]:
                minims+=[minims2[-1]]
            elif maxims[0]!=maxims2[0]:
                maxims=[maxims2[0]]+maxims
            else:
                maxims=maxims[:-1]
        except IndexError:
            maxims=maxims[:-1]
    print maxims,minims
    return maxims,minims
