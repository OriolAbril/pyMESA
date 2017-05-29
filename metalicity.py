import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
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

nonmetals=[]
metals=[]
abunPat = re.compile(r'([a-z]{1,3})[0-9]{1,3}$',re.IGNORECASE)
start=0
end=200
length=len(models)
Z1vec=np.arange(length, dtype=float)
agevec=np.arange(length, dtype=float)
# load which metalic and nonmetalic isotopes are present
doc=''.join([log_fold, '/profile1.data'])  # it does not need to be the first model
# all profiles have the same columns
hdr, cols, data=pym.readProfileFast(doc)
abun_list=pym.getIsos(cols.keys())
for iso in abun_list:
    abunMatch = abunPat.match(iso)
    el = abunMatch.groups(1)[0]
    if np.any(np.array(['h', 'he'])==el):
        nonmetals.append(iso)
    else:
        metals.append(iso)
# iterate over all profiles to calculate metallicity
for i,mod_num in enumerate(models):
    doc=''.join([log_fold, '/profile', str(profs[mod_num]), '.data'])
    hdr, cols, data=pym.readProfileFast(doc)
    Z1=0.
    w=10**data[:,cols['logdq']]  # get mass fractions
    wsum=sum(w[start:end])
    # Add all mass fractions (with respect to the cell) for h and he
    for iso in nonmetals:
        Z1+=data[:,cols[iso]][start:end]
    # Use cell mass fraction (with respect to the total mass) as weight 
    # for th average metallicity
    Z1*=w[start:end]
    Z1=sum(Z1)/wsum
    Z1vec[i]=1-Z1
    agevec[i]=hdr['star_age']

plt.plot(agevec,Z1vec)
plt.show()
