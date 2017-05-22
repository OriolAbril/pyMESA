import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('/home/oriol/Publico/mesaplot/mesaPlot')
import file_reader as mp
#import mesaPlot as mp
import re

m=mp.MESA()

log_fold='LOGS'
# find all profiles to import with mesaPlot
m._loadProfileIndex(log_fold)
profiles = m.prof_ind['profile']
first=True
nonmetals=[]
metals=[]
abunPat = re.compile(r'([a-z]{1,3})[0-9]{1,3}$',re.IGNORECASE)
start=0
end=200
Z1vec=np.arange(len(profiles),dtype=float)
Z2vec=np.arange(len(profiles),dtype=float)
agevec=np.arange(len(profiles),dtype=float)
for i,prof in enumerate(profiles):
    m.loadProfile(f=log_fold, prof=prof, silent=True)
    if first:
        abun_list=pym.getIsos(m.prof.data_names)
        for iso in abun_list:
            abunMatch = abunPat.match(iso)
            el = abunMatch.groups(1)[0]
            if np.any(np.array(['h','he'])==el):
                nonmetals.append(iso)
            else:
                metals.append(iso)
        first=False
    dat=m.prof.data
    Z1=0.
    w=10**dat['logdq']  # get mass fractions
    wsum=sum(w[start:end])
    # Add all mass fractions (with respect to the cell) for h and he
    for iso in nonmetals:
        Z1+=dat[iso][start:end]
    # Use cell mass fraction (with respect to the total mass) as weight 
    # for th average metallicity
    Z1*=w[start:end]
    Z1=sum(Z1)/wsum
    Z1vec[i]=1-Z1
    Z2=0.
    # Add all mass fractions (with respect to the cell) for metals 
    for iso in metals:
        Z2+=dat[iso][start:end]
    # Use cell mass fraction (with respect to the total mass) as weight 
    # for th average metallicity
    Z2*=w[start:end]
    Z2vec[i]=sum(Z2)/wsum
    agevec[i]=m.prof.head['star_age']
plt.plot(agevec,Z1vec,agevec,Z2vec)
plt.show()
