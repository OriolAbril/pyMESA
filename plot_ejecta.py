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

nonmetals=['h1','h2','h3','he3','he4']

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
if abun_list[-1][-1]=='\n':
    abun_list[-1]=abun_list[-1][:-1]
unstable_list=[iso for iso in abun_list if iso not in pym.stable_isos]
stable_list=[iso for iso in abun_list if iso in pym.stable_isos]
#analyze_list=['he3','ne22','li6','s36','li7','b10','be9']
analyze_list=abun_list
analyze_indexs=[abun_list.index(iso) for iso in analyze_list]
amasses=[int(i[1]) for i in re.findall(pym.abunPat,line)]
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
ax1.grid(True)
ax1.set_title('Chemical composition of the ejected material')

fig2=plt.figure(2)
ax2=fig2.add_subplot(111)
for j in xrange(shape[0]):
    pymp.plotAbunByA(ax2,analyze_list,ejected_mass[j,analyze_indexs],color=colors[j],solar=True)
    #pymp.plotAbunText(ax2,abun_list,ejected_mass[j,:],amasses,color=colors[j],solar=True)
ax2.legend(loc='upper left',handles=leg)
ax2.grid(True)
ax2.set_title('Chemical composition of the ejected material compared to solar abundances')

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
ax3.set_xlabel('Burst number')
ax3.set_ylabel('Ejected mass fraction')
ax3.grid(True)
#ax3.set_title('Ejected mass')

fig4=plt.figure(4)
ax4=fig4.add_subplot(111)
for iso in analyze_list:
    i=abun_list.index(iso)
    mean=np.mean(ejected_mass[:,i])
    if mean>1e-15:
        ax4.plot(bursts,ejected_mass[:,i]/ejected_mass[0,i],label=iso)
        ax4.text(bursts[-1],ejected_mass[-1,i]/ejected_mass[0,i],iso)
ax4.set_yscale('log')
#ax4.legend()
ax4.set_xlabel('Burst number')
ax4.set_ylabel('Ejected mass fraction relative to 1st burst')
ax4.grid(True)
#ax4.set_title('Ejected mass')

fig5=plt.figure(5)
ax5=fig5.add_subplot(111)
unstable_index=[abun_list.index(iso) for iso in unstable_list]
stable_index=[abun_list.index(iso) for iso in stable_list]
ax5.plot(bursts,np.sum(ejected_mass[:,unstable_index],axis=1)/np.sum(ejected_mass[0,unstable_index]),label='Unstable elements')
ax5.plot(bursts,np.sum(ejected_mass[:,stable_index],axis=1)/np.sum(ejected_mass[0,stable_index]),label='Stable elements')
ax5.plot(bursts,np.sum(ejected_mass[:,:],axis=1)/np.sum(ejected_mass[0,:]),label='All elements')
ax5.set_yscale('log')
ax5.legend()
ax5.grid(True)
ax5.set_xlabel('Burst number')
ax5.set_ylabel('Mass fraction')
ax5.set_ylim([0.2, 5])
#ax5.set_title('')

fig6=plt.figure(6)
ax5=fig6.add_subplot(111)
num_bursts=np.shape(ejected_mass)[0]
metallicity=np.zeros(num_bursts)
for j in xrange(num_bursts):
    total=0
    for i,iso in enumerate(abun_list):
        if iso not in nonmetals:
            metallicity[j]+=ejected_mass[j,i]
            total+=ejected_mass[j,i]
        else:
            total+=ejected_mass[j,i]
    print total
ax5.plot(bursts,metallicity,linewidth=1,markersize=2.5)
ax5.set_xlabel('Burst number')
ax5.set_ylabel('Metallicity')
ax5.grid(True)


plt.show()
