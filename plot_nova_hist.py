import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FormatStrFormatter
from NuGridPy import mesa as ms
import re
from astropy import constants
import argparse as arp  # command line parsing module and help

p=arp.ArgumentParser(description='Script to save and plot data from nova bursts simulated with MESA')
p.add_argument('folder', help='Path to the LOGS folder', default='LOGS')
args=p.parse_args()  # parse arguments

log_fold=args.folder

# load history and identify bursts
length=pym.file_len('%s/history.data' %log_fold)
hhdr, hcols, hdata=ms._read_mesafile('%s/history.data' %log_fold, length-6)
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

fig1=plt.figure(1)
ax1=fig1.add_axes([0.2,0.15,0.7,0.7])
ax1.plot(star_age,star_mass,'k')
ax1.set_xlabel('Star age (years)')
ax1.set_ylabel('Star mass ($M_{\odot}$)')
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax1.grid(True)

x=np.arange(len(maxims))+1
fig2=plt.figure(2)
ax21=fig2.add_axes([0.2,0.55,0.7,0.35])
ax21.plot(x[:-1]+0.5,recurrence,'o-')
ax21.grid(True)
ax21.set_ylabel('Recurrence time\n(years)')
plt.setp(ax21.get_xticklabels(), visible=False)
ax21.xaxis.set_ticks_position('none')
ax22=fig2.add_axes([0.2,0.15,0.7,0.35], sharex=ax21)
ax22.grid(True)
ax22.plot(x,eject_mass,'o-')
ax22.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
ax22.set_xlabel('Burst number')
ax22.set_ylabel('Ejected mass ($M_{\odot}$)')

fig3=plt.figure(3)
ax3=fig3.add_axes([0.1,0.13,0.83,0.77])
log_Teff=hdata[:,hcols['log_Teff']-1]
log_L=hdata[:,hcols['log_L']-1]
ax3.plot(log_Teff[:minims[0]],log_L[:minims[0]],label='burst num %d' %1,linewidth=1)
for i in range(len(minims)-1):
    ax3.plot(log_Teff[minims[i]:minims[i+1]],log_L[minims[i]:minims[i+1]], label='burst num %d' %(i+2),
             linewidth=1)
ax3.legend()
ax3.grid(True)
#ax3.set_ylim([-3,8.5])
#ax3.set_xlim([4.5,7])
ax3.invert_xaxis()
ax3.set_xlabel('$\log(T_{eff})$')
ax3.set_ylabel('$\log(L)$')

fig4=plt.figure(4)
ax4=fig4.add_axes([0.15,0.13,0.77,0.77])
ax4.plot(star_age,log_Teff,'k',linewidth=1)
ax4.set_xlabel('Star age (years)')
ax4.set_ylabel('$\log(T_{eff})$')
ax4.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax4.grid(True)

fig5=plt.figure(5)
ax5=fig5.add_axes([0.15,0.13,0.77,0.77])
ax5.plot(star_age,log_L,'k',linewidth=1)
ax5.set_xlabel('Star age (years)')
ax5.set_ylabel('$\log(L)$')
ax5.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax5.grid(True)

plt.show()
