import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib as mpl
from cycler import cycler
mpl.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from NuGridPy import mesa as ms
import re
from astropy import constants
import argparse as arp  # command line parsing module and help

paths=['/media/oriol/Elements/oriol/TFG-Novae/Tests/ONe/']*4
paths[0]+='cno_extras_o18_to_mg26_plus_fe56_net/o-ne_nova_multiple_burst_all_profiles/'
paths[1]+='nova_net/10bursts_1.3M/'
paths[2]+='nova_modified_net/10bursts_1.3M'
paths[3]+='jj_thesis_isos/10bursts_1.3M'
names=['cno_1.3M', 'nova_net_1.3M', 'nova_mod_1.3M', 'jj_isos_1.3M']
labels=['cno', 'nova_ext', 'nova_mod', 'jj_isos']

# initialize axes and figures
fig1=plt.figure(1)
ax1=fig1.add_axes([0.2,0.15,0.7,0.7])
fig2=plt.figure(2)
ax21=fig2.add_axes([0.2,0.54,0.7,0.37])
ax22=fig2.add_axes([0.2,0.15,0.7,0.37], sharex=ax21)
fig3=plt.figure(3)
ax3=fig3.add_axes([0.1,0.13,0.83,0.77])
fig4=plt.figure(4)
ax4=fig4.add_axes([0.15,0.15,0.75,0.75])
nonmetals=['h1','h2','h3','he3','he4']
for f,path in enumerate(paths):
    # load history and identify bursts
    length=pym.file_len('%s/LOGS/history.data' %path)
    hhdr, hcols, hdata=ms._read_mesafile('%s/LOGS/history.data' %path, length-6)
    star_age=hdata[:,hcols['star_age']-1]
    model_numbers=hdata[:,hcols['model_number']-1]
    star_mass=hdata[:,hcols['star_mass']-1]
    hlength=len(star_age)
    maxims, minims=pym.getExtremes(star_mass, rng=100)
    if len(maxims)==len(minims)+1:
        maxims2, minims2=pym.getExtremes(star_mass, rng=5)
        try:
            if minims[-1]!=minims2[-1]:
                minims+=[minims2[-1]]
            else:
                maxims=maxims[:-1]
        except IndexError:
            maxims=maxims[:-1]
    
    if len(maxims)!=len(minims):
        raise IndexError('Found different number of maximumns and minimums\nTry modifying the comparison ranges')
    
    recurrence=star_age[maxims[1:]]-star_age[maxims[:-1]]
    eject_mass=star_mass[maxims]-star_mass[minims]
    
    ax1.plot(star_age,star_mass,label=labels[f])
    
    x=np.arange(len(maxims))+1
    ax21.plot(x[:-1]+0.5,recurrence,'o-',linewidth=1,markersize=2.5,label=labels[f])
    ax22.plot(x,eject_mass,'o-',linewidth=1,markersize=2.5)
    
    log_Teff=hdata[:,hcols['log_Teff']-1]
    log_L=hdata[:,hcols['log_L']-1]
    ax3.plot(log_Teff,log_L,label=labels[f],linewidth=1)

    # load .dat and .txt output files from ejecta.py
    ejected_mass=np.loadtxt('%s/%s.dat' %(path,names[f]))[:,:]
    tfile=open('%s/%s.txt' %(path,names[f]),'r')
    line=tfile.readline()
    tfile.close()
    line=line.replace(':',',')
    abun_list=line.split(',')[1:]
    if abun_list[-1][-1]=='\n':
        abun_list[-1]=abun_list[-1][:-1]
    num_bursts=np.shape(ejected_mass)[0]
    metallicity=np.zeros(num_bursts)
    for j in xrange(num_bursts):
        for i,iso in enumerate(abun_list):
            if iso not in nonmetals:
                metallicity[j]+=ejected_mass[j,i]
    ax4.plot(x,metallicity,label=labels[f],linewidth=1,markersize=2.5)

# customize plots
ax1.set_xlabel('Star age (years)')
ax1.set_ylabel('Star mass ($M_{\odot}$)')
ax1.legend()
ax1.grid(True)
ax21.grid(True)
ax21.set_ylabel('Recurrence time\n(years)')
plt.setp(ax21.get_xticklabels(), visible=False)
ax21.xaxis.set_ticks_position('none')
ax21.legend()
ax22.grid(True)
ax22.set_xlabel('Burst number')
ax22.set_ylabel('Ejected mass ($M_{\odot}$)')
ax3.legend()
ax3.grid(True)
ax3.set_ylim([-3,8.5])
ax3.set_xlim([4.5,7])
ax3.invert_xaxis()
ax3.set_xlabel('$\log(T_{eff})$')
ax3.set_ylabel('$\log(L)$')
ax4.legend()
ax4.set_xlabel('Burst number')
ax4.set_ylabel('Metallicity')
ax4.grid(True)
plt.show()
