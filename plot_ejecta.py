import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import pyMESAplotutils as pymp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from NuGridPy import mesa as ms
import re
from astropy import constants
import argparse as arp  # command line parsing module and help


abunPat=re.compile(r'([a-z]{1,3})([0-9]{1,3})',re.IGNORECASE)
def plotAbunByA(ax,isos_list,ejected_mass,color=None,solar=False):
# create dictionary containing the isotopes for each element
    eldict={}
    amasses=range(len(isos_list))
    for i,iso in enumerate(isos_list):
        m=abunPat.match(iso)
        amasses[i]=int(m.groups(1)[1])
        el=m.groups(1)[0]
        try:
            eldict[el]+=[iso]
        except KeyError:
            eldict[el]=[iso]
    else:
        eldict[el]=sorted(eldict[el])
    for k,el in enumerate(eldict):
        masses=[]
        ej_iso=[]
        for iso in eldict[el]:
            i=isos_list.index(iso)
            if solar:
                if iso in pym.stable_isos:
                    solar=pym.sol_comp_ag89[pym.stable_isos.index(iso)]
                    ej_iso.append(ejected_mass[i]/solar)
                    masses.append(amasses[i])
            else:
                ej_iso.append(ejected_mass[i])
                masses.append(amasses[i])
        line, =ax.plot(masses, ej_iso, 'o-', color=color, linewidth=0.5, markersize=1)
        ytextval=np.max(ej_iso)
        xtextval=masses[ej_iso.index(ytextval)]
        ax.text(xtextval,ytextval,el,color=color,clip_on=True)
    ax.set_yscale('log')
    ax.set_xlim([0, max(amasses)+1])
    if solar:
        ax.set_ylim([1e-10, 1e3])
    else:
        ax.set_ylim([1e-10, 1.5])

def plotAbunText(ax,isos_list,ejected_mass,amasses,color=None,solar=False):
    for i,iso in enumerate(isos_list):
        if solar:
            if iso in pym.stable_isos:
                solar=pym.sol_comp_ag89[pym.stable_isos.index(iso)]
                ax.text(amasses[i], ejected_mass[i]/solar, iso, color=colors[j], clip_on=True)
        else:
            ax.text(amasses[i], ejected_mass[i], iso, color=colors[j], clip_on=True)
    plt.yscale('log')
    plt.axis([0, max(amasses)+3, 1e-1, 1e4])

p=arp.ArgumentParser(description='Script to save and plot data from nova bursts simulated with MESA')
p.add_argument('filename', help='Name of the files to save')
args=p.parse_args()  # parse arguments

#analyze_list=['o14','o15','o16','o17','ne20','ne22']
colors=[p['color'] for p in plt.rcParams['axes.prop_cycle']]
ejected_mass=np.loadtxt(args.filename+'.dat')[:,:]
f=open(args.filename+'.txt','r')
line=f.readline()
f.close()
line=line.replace(':',',')
abun_list=line.split(',')[1:]
unstable_list=[iso for iso in abun_list if iso not in pym.stable_isos]
stable_list=[iso for iso in abun_list if iso in pym.stable_isos]
analyze_list=unstable_list
analyze_indexs=[abun_list.index(iso) for iso in analyze_list]
amasses=[int(i[1]) for i in re.findall(abunPat,line)]
shape=np.shape(ejected_mass)
bursts=np.arange(1,shape[0]+1)
leg=[]
fig1=plt.figure(1)
ax1=fig1.add_subplot(111)
for j in xrange(shape[0]):
    leg.append(mlines.Line2D([], [], color=colors[j], label='Burst num %d' %(j+1)))
    pymp.plotAbunByA(ax1,analyze_list,ejected_mass[j,analyze_indexs],color=colors[j],solar=False)
    #pymp.plotAbunText(ax1,abun_list,ejected_mass[j,:],amasses,color=colors[j],solar=False)
ax1.legend(handles=leg)


fig2=plt.figure(2)
ax2=fig2.add_subplot(111)
for j in xrange(shape[0]):
    pymp.plotAbunByA(ax2,analyze_list,ejected_mass[j,analyze_indexs],color=colors[j],solar=False)
    #pymp.plotAbunText(ax2,abun_list,ejected_mass[j,:],amasses,color=colors[j],solar=True)
ax2.legend(loc='upper left',handles=leg)

fig3=plt.figure(3)
ax3=fig3.add_subplot(111)
for iso in analyze_list:
    i=abun_list.index(iso)
    mean=np.mean(ejected_mass[:,i])
    if mean>1e-15:
        ax3.plot(bursts,ejected_mass[:,i],label=iso)
        ax3.text(bursts[-1],ejected_mass[-1,i],iso)
        ax3.text(bursts[0],ejected_mass[0,i],iso)
ax3.set_yscale('log')
ax3.legend()

fig4=plt.figure(4)
ax4=fig4.add_subplot(111)
for iso in analyze_list:
    i=abun_list.index(iso)
    mean=np.mean(ejected_mass[:,i])
    if mean>1e-15:
        ax4.plot(bursts,ejected_mass[:,i]/ejected_mass[0,i],label=iso)
        ax4.text(bursts[-1],ejected_mass[-1,i]/ejected_mass[0,i],iso)
ax4.set_yscale('log')
ax4.legend()

fig5=plt.figure(5)
ax5=fig5.add_subplot(111)
unstable_index=[abun_list.index(iso) for iso in unstable_list]
stable_index=[abun_list.index(iso) for iso in stable_list]
ax5.plot(bursts,np.sum(ejected_mass[:,unstable_index],axis=1),label='Unstable elements')
ax5.plot(bursts,np.sum(ejected_mass[:,stable_index],axis=1),label='Stable elements')
ax5.plot(bursts,np.sum(ejected_mass[:,:],axis=1),label='All elements')
ax5.set_yscale('log')
ax5.legend()

plt.show()
