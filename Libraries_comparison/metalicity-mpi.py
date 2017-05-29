import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib.pyplot as plt
from NuGridPy import mesa as ms
import re
import multiprocessing as mpi

log_fold='LOGS'
p=ms.mesa_profile()
# find all profiles to import 
p._profiles_index()
models=p.model
profs=p.log_ind

threads=4
start=0
end=200
nonmetals=[]
metals=[]
abunPat = re.compile(r'([a-z]{1,3})[0-9]{1,3}$',re.IGNORECASE)
length=len(models)
Zvec=np.arange(length, dtype=float)
agevec=np.arange(length, dtype=float)

doc=''.join([log_fold, '/profile', str(profs[models[0]]), '.data'])
length=pym.file_len(doc)
hdr, cols, data=ms._read_mesafile(doc, length-6)
abun_list=pym.getIsos(cols.keys())
for iso in abun_list:
    abunMatch = abunPat.match(iso)
    el = abunMatch.groups(1)[0]
    if np.any(np.array(['h', 'he'])==el):
        nonmetals.append(iso)
    else:
        metals.append(iso)

def getZ(mod_num, profs=profs, start=start, end=end):
    doc=''.join([log_fold, '/profile', str(profs[mod_num]), '.data'])
    f=open(doc,'r')
    line1,line2,line3=[f.readline() for line in xrange(3)]
    f.close()
    line2list=line2.split()
    line3list=line3.split()
    length=int(line3list[line2list.index('num_zones')])
    hdr, cols, data=ms._read_mesafile(doc, length)
    Z=0.
    w=10**data[:,cols['logdq']-1]  # get mass fractions
    # Add all mass fractions (with respect to the cell) for h and he
    for iso in nonmetals:
        Z+=data[:,cols[iso]-1][start:end]
    # Use cell mass fraction (with respect to the total mass) as weight 
    # for th average metallicity
    Z*=w[start:end]
    Z=1.-sum(Z)/sum(w[start:end])
    age=hdr['star_age']
    return age,Z

pool= mpi.Pool(processes=threads)
result=pool.map(getZ, models)
pool.close()
pool.join()

agevec[:]=[a[0] for a in result]
Zvec[:]=[a[1] for a in result]
plt.plot(agevec,Zvec)
#plt.show()
