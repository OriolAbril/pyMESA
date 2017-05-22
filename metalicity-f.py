import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import reader as rd
import numpy as np
import matplotlib.pyplot as plt
from NuGridPy import mesa as ms
import re

log_fold='LOGS'
p=ms.mesa_profile()
# find all profiles to import 
p._profiles_index()
models=p.model
profs=p.log_ind

first=True
nonmetals=[]
metals=[]
abunPat = re.compile(r'([a-z]{1,3})[0-9]{1,3}$',re.IGNORECASE)
start=0
end=200
length_mod=len(models)
Zvec=np.arange(length_mod, dtype=float)
agevec=np.arange(length_mod, dtype=float)
# read first file to initialize and allocate vars
doc=''.join([log_fold, '/profile', str(profs[models[0]]), '.data'])
length=pym.file_len(doc)
hdr, cols, data=ms._read_mesafile(doc, length-6)
abun_list=pym.getIsos(cols.keys())
columns=len(cols)
for iso in abun_list:
    abunMatch = abunPat.match(iso)
    el = abunMatch.groups(1)[0]
    if np.any(np.array(['h', 'he'])==el):
        nonmetals.append(iso)
    else:
        metals.append(iso)

for i,mod_num in enumerate(models):
    doc=''.join([log_fold, '/profile', str(profs[mod_num]), '.data'])
    f=open(doc,'r')
    line1,line2,line3=[f.readline() for line in xrange(3)]
    f.close()
    line2list=line2.split()
    line3list=line3.split()
    length=int(line3list[line2list.index('num_zones')])
    data=np.empty((length,columns))
    data=rd.readmesafile(doc,7,length,columns)
    Z=np.zeros(end-start)
    w=10**data[:,cols['logdq']-1]  # get mass fractions
    wsum=sum(w[start:end])
    # Add all mass fractions (with respect to the cell) for h and he
    for iso in nonmetals:
        Z+=data[:,cols[iso]-1][start:end]
    # Use cell mass fraction (with respect to the total mass) as weight 
    # for th average metallicity
    Z*=w[start:end]
    Z=sum(Z)/wsum
    Zvec[i]=1-Z
    agevec[i]=line3list[line2list.index('star_age')]

plt.plot(agevec,Zvec)
plt.show()
