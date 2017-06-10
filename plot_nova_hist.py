import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib as mpl
from cycler import cycler
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.ticker import FormatStrFormatter
from NuGridPy import mesa as ms
import re
from astropy import constants
import argparse as arp  # command line parsing module and help

p=arp.ArgumentParser(description='Script to save and plot data from nova bursts simulated with MESA')
p.add_argument('folder', help='Path to the LOGS folder', nargs='+')
p.add_argument('-l','--labels', help='Labels of each file', nargs='+')
args=p.parse_args()  # parse arguments

if not(args.labels):
    args.labels=args.folder
linestyle=['-','--','-.',':',(0,(5, 1.5, 1, 1.5, 1, 1.5))]
linestyle=cycler(linestyle=linestyle)
fig1=plt.figure(1)
ax1=fig1.add_axes([0.2,0.15,0.7,0.7])
fig2=plt.figure(2)
ax21=fig2.add_axes([0.2,0.55,0.7,0.35])
ax22=fig2.add_axes([0.2,0.15,0.7,0.35], sharex=ax21)
fig3=plt.figure(3)
ax3=fig3.add_axes([0.1,0.13,0.83,0.77])
fig31=plt.figure(6)
ax31=fig31.add_axes([0.1,0.13,0.83,0.77])
fig4=plt.figure(4)
ax4=fig4.add_axes([0.15,0.13,0.77,0.77])
fig5=plt.figure(5)
ax5=fig5.add_axes([0.15,0.13,0.77,0.77])
leg=[]

for flabel,log_fold,lstyle in zip(args.labels,args.folder,linestyle()):
    # load history and identify bursts
    ls=lstyle['linestyle']
    length=pym.file_len('%s/history.data' %log_fold)
    hhdr, hcols, hdata=ms._read_mesafile('%s/history.data' %log_fold, length-6)
    star_age=hdata[:,hcols['star_age']-1]
    model_numbers=hdata[:,hcols['model_number']-1]
    star_mass=hdata[:,hcols['star_mass']-1]
    hlength=len(star_age)
    maxims,minims=pym.getMaxsMins(star_mass,250,10)
    if len(maxims)!=len(minims):
        maxims,minims=pym.getMaxsMins(star_mass,50,5)
    if len(maxims)!=len(minims):
        maxims,minims=pym.getMaxsMins(star_mass,500,50)
    if len(maxims)!=len(minims):
        raise IndexError('Found different number of maximumns and minimums\nTry modifying the comparison ranges')

    recurrence=star_age[maxims[1:]]-star_age[maxims[:-1]]
    eject_mass=star_mass[maxims]-star_mass[minims]

    ax1.plot(star_age,star_mass,label=flabel)
    x=np.arange(len(maxims))+1
    ax21.plot(x[:-1]+0.5,recurrence,'o-',label=flabel)
    ax22.plot(x,eject_mass,'o-',label=flabel)

    log_Teff=hdata[:,hcols['log_Teff']-1]
    log_L=hdata[:,hcols['log_L']-1]
    ax31.plot(log_Teff,log_L,label=flabel)
    ax3.plot(log_Teff[:minims[0]],log_L[:minims[0]], ls=ls, linewidth=1)
    leg.append(mlines.Line2D([], [], ls=ls, color='k',linewidth=1, label=flabel))
    for i in range(len(minims)-1):
        ax3.plot(log_Teff[minims[i]:minims[i+1]],log_L[minims[i]:minims[i+1]], linewidth=1, ls=ls)

    ax4.plot(star_age,log_Teff,linewidth=1,label=flabel)
    ax5.plot(star_age,log_L,linewidth=1,label=flabel)

# Create a legend for the first line.
first_legend=ax3.legend(handles=leg, handlelength=3, loc='upper right')
leg2=[]
colors=[p['color'] for p in plt.rcParams['axes.prop_cycle']]
for j in range(10):
    leg2.append(mlines.Line2D([], [], linestyle='-', color=colors[j],linewidth=1,  label='burst num %d' %(j+1)))
ax1.legend()
ax1.set_xlabel('Star age (years)')
ax1.set_ylabel('Star mass ($M_{\odot}$)')
ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax1.grid(True)
ax21.grid(True)
ax21.legend()
ax21.set_ylabel('Recurrence time\n(years)')
plt.setp(ax21.get_xticklabels(), visible=False)
ax21.xaxis.set_ticks_position('none')
ax22.grid(True)
ax22.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
ax22.set_xlabel('Burst number')
ax22.set_ylabel('Ejected mass ($M_{\odot}$)')
ax3.grid(True)
# Add the legend manually to the current Axes.
ax = ax3.add_artist(first_legend)
ax3.legend(handles=leg2,loc='lower left')
#ax3.set_ylim([-3,8.5])
#ax3.set_xlim([4.5,7])
ax3.invert_xaxis()
ax3.set_xlabel('$\log(T_{eff})$')
ax3.set_ylabel('$\log(L)$')
ax31.grid(True)
ax31.legend()
ax31.invert_xaxis()
ax31.set_xlabel('$\log(T_{eff})$')
ax31.set_ylabel('$\log(L)$')
ax4.legend()
ax4.set_xlabel('Star age (years)')
ax4.set_ylabel('$\log(T_{eff})$')
ax4.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax4.grid(True)
ax5.legend()
ax5.set_xlabel('Star age (years)')
ax5.set_ylabel('$\log(L)$')
ax5.xaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax5.grid(True)
plt.show()
