import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from NuGridPy import mesa as ms
import re
from astropy import constants
import argparse as arp  # command line parsing module and help

p=arp.ArgumentParser(description='Script to save and plot data from nova bursts simulated with MESA')
p.add_argument('filename', help='Name of the files to save')
p.add_argument('-f', '--folder', help='Name of the log folder', default='LOGS')
p.add_argument('-b', '--bursts', help='Number of bursts to find', default=10,type=int)
p.add_argument('-r', '--range', help='Range for the subroutine that finds the maximums and\
               minimums',type=int,nargs=2,default=[100,10])
args=p.parse_args()  # parse arguments

log_fold=args.folder
p=ms.mesa_profile(sldir=log_fold)
# find all profiles to import 
p._profiles_index()
models=np.array(p.model)
profs=p.log_ind
# initialize variables
first=True
nonmetals=[]
metals=[]
abunPat = re.compile(r'([a-z]{1,3})([0-9]{1,3})$',re.IGNORECASE)
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
maxims,minims=pym.getMaxsMins(star_mass,args.range[0],args.range[1],num_bursts=args.bursts)
#if len(maxims)!=len(minims):
#    maxims,minims=pym.getMaxsMins(star_mass,50,5)
#    print '50'
#if len(maxims)!=len(minims):
#    maxims,minims=pym.getMaxsMins(star_mass,500,50)
#    print '500'
if len(maxims)!=len(minims):
    raise IndexError('Found different number of maximumns (%d) and minimums(%d)\nTry modifying the\
            comparison ranges' %(len(maxims),len(minims)))

recurrence=star_age[maxims[1:]]-star_age[maxims[:-1]]
print 'Recurrence time:', recurrence
eject_mass=star_mass[maxims]-star_mass[minims]
print 'Ejected mass:', eject_mass
plt.figure(1)
plt.plot(star_age,star_mass,'k',star_age[maxims],star_mass[maxims],'ro')
plt.plot(star_age[minims],star_mass[minims],'bo')
x=range(len(maxims))
plt.figure(2)
plt.subplot(211)
plt.plot(x[:-1],recurrence,'o-')
plt.subplot(212)
plt.plot(x,eject_mass,'o-')
plt.figure(3)
log_Teff=hdata[:,hcols['log_Teff']-1]
log_L=hdata[:,hcols['log_L']-1]
plt.plot(log_Teff[:minims[0]],log_L[:minims[0]],label='burst num %d' %1)
for i in range(len(minims)-1):
    plt.plot(log_Teff[minims[i]:minims[i+1]],log_L[minims[i]:minims[i+1]], label='burst num %d' %(i+2))
plt.legend()
plt.show()
#plt.pause(2)
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

Tmax=np.zeros(len(burstsind))-40
vels=np.zeros((len(burstsind),2))
for j,burst in enumerate(burstsind):
    doc=''.join([log_fold, '/profile', str(profs[burst[0]]), '.data'])
    hdr, cols, data=pym.readProfileFast(doc)
    w=10.**data[:,cols['logdq']]  # get mass fractions
    ejecsum=0
    ejecmass=0
    maxV=0
    minV=1e99
    for i,mod_num in enumerate(burst[1:]):
        hdr_old=hdr; cols_old=cols; data_old=data
        doc=''.join([log_fold, '/profile', str(profs[mod_num]), '.data'])
        hdr, cols, data=pym.readProfileFast(doc)
        logTemp=data[:,cols['logT']]
        if max(logTemp)>Tmax[j]:
            Tmax[j]=max(logTemp)
        star_mass=hdr['star_mass']
        if first:
            abun_list=pym.getIsos(cols.keys())
            amasses=[]
            for iso in abun_list:
                abunMatch = abunPat.match(iso)
                el = abunMatch.groups(1)[0]
                amasses.append(int(abunMatch.groups(1)[1]))
                if np.any(np.array(['h', 'he'])==el):
                    nonmetals.append(iso)
                else:
                    metals.append(iso)
            ejected_mass=np.zeros((len(burstsind), len(abun_list)))
            first=False
        Z1=0.
        wold=w
        w=10.**data[:,cols['logdq']]  # get mass fractions
        # Add all mass fractions (with respect to the cell) for h and he
        #print mod_num
        wsum=0
        modejecta=np.zeros(len(abun_list))
        eject=False
        noeject=0
        for cell,speed in enumerate(data[:,cols['velocity']]):
            M=(1.-10.**data[cell,cols['logxq']])*star_mass*Msun
            escapev=np.sqrt(2.*G*M/(data[cell,cols['radius']]*Rsun))
            #print(escapev, speed)
            if escapev<speed:  # check if ejected
                eject=True
                #print speed,escapev
                if speed>maxV:
                    maxV=speed*1.
                elif speed<minV:
                    minV=speed*1.
                #print maxV,minV
                protoejecta=np.array([data[cell,cols[iso]] for iso in abun_list],dtype=float)
                protoejecta*=w[cell] #calculate ejected mass fractions
                modejecta+=protoejecta
                wsum+=w[cell]
                #pym.terminal_print([(iso,data[cell,cols[iso]]) for iso in abun_list])
            else:
                noeject+=1
                if noeject>10:
                    #print(len(w), cell)
                    break
        if eject:
            #print sum(modejecta/wsum)
            ejected_mass[j,:]+=modejecta/wsum
            ejecsum+=1
            ejecmass+=wsum*star_mass
    print ejecmass, eject_mass[j]
    ejected_mass[j,:]=ejected_mass[j,:]/ejecsum
    vels[j,0]=maxV
    vels[j,1]=minV

colors=[p['color'] for p in plt.rcParams['axes.prop_cycle']]
np.savetxt(args.filename+'.dat',ejected_mass)
f=open(args.filename+'.txt','w')
f.write('Elements:'+','.join(abun_list))
f.write('\nMaximum temperature:'+','.join([str(t) for t in Tmax]))
f.write('\nMaximum velocity:'+','.join([str(v) for v in vels[:,0]]))
f.write('\nMinimum:'+','.join([str(v) for v in vels[:,1]]))
f.write('\n# Models in each burst\n')
f.write('\n'.join([','.join([str(mod) for mod in burst]) for burst in burstsind]))
f.close()
