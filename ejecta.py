import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib.pyplot as plt
from NuGridPy import mesa as ms
import re
from astropy import constants

log_fold='LOGS'
p=ms.mesa_profile()
# find all profiles to import 
p._profiles_index()
models=np.array(p.model)
profs=p.log_ind
# initialize variables
first=True
nonmetals=[]
metals=[]
abunPat = re.compile(r'([a-z]{1,3})[0-9]{1,3}$',re.IGNORECASE)
start=0
length=len(models)
Z1vec=np.arange(length, dtype=float)
agevec=np.arange(length, dtype=float)
G=constants.G._value
Rsun=constants.R_sun._value
Msun=constants.M_sun._value

# load history and identify bursts
length=pym.file_len('%s/history.data' %log_fold)
hhdr, hcols, hdata=ms._read_mesafile('%s/history.data' %log_fold, length-6)
star_age=hdata[:,hcols['star_age']-1]
model_numbers=hdata[:,hcols['model_number']-1]
star_mass=hdata[:,hcols['star_mass']-1]
hlength=len(star_age)
maxims, minims=pym.getExtremes(star_mass, rng=80)
if len(maxims)==len(minims)+1:
    maxims2, minims2=pym.getExtremes(star_mass, rng=10)
    minims+=[minims2[-1]]
if len(maxims)!=len(minims):
    raise IndexError('Found different number of maximumns and minimums\n\
                     Try modifying the comparison ranges')

recurrence=star_age[maxims[1:]]-star_age[maxims[:-1]]
print 'Recurrence time:', recurrence
ejected_mass=star_mass[maxims]-star_mass[minims]
print 'Ejected mass:', ejected_mass
plt.figure(1)
plt.plot(star_age,star_mass,'k',star_age[maxims],star_mass[maxims],'ro')
plt.plot(star_age[minims],star_mass[minims],'bo')
x=range(len(maxims))
plt.figure(2)
plt.subplot(211)
plt.plot(x[:-1],recurrence,'o-')
plt.subplot(212)
plt.plot(x,ejected_mass,'o-')
#plt.show()
plt.pause(0.5)
model_maxims=model_numbers[maxims]
model_minims=model_numbers[minims]
burstsind=range(len(maxims))  # save index positions for all profiles corresponding to a burst
burst=[]
j=0
init_burst=model_maxims[0]
end_burst=model_minims[0]
for mod_num in models:
    if mod_num>end_burst:
        burstsind[j]=burst
        j+=1
        try:
            init_burst=model_maxims[j]
            end_burst=model_minims[j]
            burst=[]
        except IndexError:
            break
    elif mod_num>init_burst:
        burst.append(mod_num)

for j,burst in enumerate(burstsind):
    doc=''.join([log_fold, '/profile', str(profs[burst[0]]), '.data'])
    hdr, cols, data=pym.readProfileFast(doc)
    w=10.**data[:,cols['logdq']]  # get mass fractions
    for i,mod_num in enumerate(burst[1:]):
        hdr_old=hdr; cols_old=cols; data_old=data
        doc=''.join([log_fold, '/profile', str(profs[mod_num]), '.data'])
        hdr, cols, data=pym.readProfileFast(doc)
        star_mass=hdr['star_mass']
        if first:
            abun_list=pym.getIsos(cols.keys())
            for iso in abun_list:
                abunMatch = abunPat.match(iso)
                el = abunMatch.groups(1)[0]
                if np.any(np.array(['h', 'he'])==el):
                    nonmetals.append(iso)
                else:
                    metals.append(iso)
            ejected_mass=np.arange(len(burstsind), len(abun_list))
            first=False
        Z1=0.
        wold=w
        w=10.**data[:,cols['logdq']]  # get mass fractions
        # Add all mass fractions (with respect to the cell) for h and he
        #print mod_num
        plt.plot(data[:,cols['radius']],data[:,cols['velocity']])
        plt.pause(0.4)
        for cell,speed in enumerate(data[:,cols['velocity']]):
            M=(1.-10.**data[cell,cols['logxq']])*star_mass*Msun
            escapev=np.sqrt(2.*G*M/(data[cell,cols['radius']]*Rsun))
            #print(escapev, speed)
            if escapev<speed:  # check if ejected
                protoejecta=np.array([(iso,data[cell,cols[iso]]) for iso in abun_list])
                protoejecta*=w[cell]*star_mass #calculate ejected mass in Msun units
                ejected_mass[j,:]+=protoejecta
                #pym.terminal_print([(iso,data[cell,cols[iso]]) for iso in abun_list])
            else:
                print(len(w), cell)
                break
        #for iso in nonmetals:
            #Z1+=data[:,cols[iso]][start:end]
        # Use cell mass fraction (with respect to the total mass) as weight 
        # for th average metallicity
        #Z1*=w[start:end]
        #Z1=sum(Z1)/wsum
        #Z1vec[i]=1-Z1
        #agevec[i]=hdr['star_age']

plt.plot(agevec,Z1vec)
plt.show()
