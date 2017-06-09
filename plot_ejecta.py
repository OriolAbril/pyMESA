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

# Define invariable quantities and objects
nonmetals=['h1','h2','h3','he3','he4']
colors=[p['color'] for p in plt.rcParams['axes.prop_cycle']]

p=arp.ArgumentParser(description='Script to save and plot data from nova bursts simulated with MESA')
p.add_argument('filename', help='Name of the files to save')
args=p.parse_args()  # parse arguments

#analyze_list=['o14','o15','o16','o17','ne20','ne22']
ejected_mass=np.loadtxt(args.filename+'.dat')[:,:]
shape=np.shape(ejected_mass)
f=open(args.filename+'.txt','r')
lines=[f.readline() for i in range(4)]
f.close()
line=lines[0].replace(':',',')
abun_list=line.split(',')[1:]
line=lines[1].replace(':',',')
Tmax=np.array([float(i) for i in line.split(',')[1:]])
line=lines[2].replace(':',',')
vels=np.empty((shape[0],2))
vels[:,0]=[float(i) for i in line.split(',')[1:]]
line=lines[3].replace(':',',')
vels[:,1]=[float(i) for i in line.split(',')[1:]]
if abun_list[-1][-1]=='\n':
    abun_list[-1]=abun_list[-1][:-1]
unstable_list=[iso for iso in abun_list if iso not in pym.stable_isos]
stable_list=[iso for iso in abun_list if iso in pym.stable_isos]
#analyze_list=['he3','ne22','li6','s36','li7','b10','be9']
analyze_list=abun_list
analyze_indexs=[abun_list.index(iso) for iso in analyze_list]
amasses=[int(i[1]) for i in re.findall(pym.abunPat,line)]
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
ax5=fig5.add_axes([0.17,0.13,0.75,0.75])
ax5.plot(bursts,Tmax,'o-')
ax5.grid(True)
ax5.set_xlabel('Burst number')
ax5.set_ylabel('$\log(T_{max})$ (K)')
#ax5.set_title('')

fig6=plt.figure(6)
ax6=fig6.add_axes([0.17,0.13,0.75,0.75])
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
ax6.plot(bursts,metallicity,linewidth=1,markersize=2.5)
ax6.set_xlabel('Burst number')
ax6.set_ylabel('Metallicity')
ax6.grid(True)

fig7=plt.figure(7)
ax7=fig7.add_subplot(111)
ax7.plot(bursts,vels[:,0],'o-',label='$v_{max}$')
ax7.plot(bursts,vels[:,1],'o-',label='$v_{min}$')
ax7.legend()
ax7.set_yscale('log')
ax7.grid(True)
ax7.set_xlabel('Burst number')
ax7.set_ylabel('Ejected cell velocity (m/s)')
#ax5.set_title('')


plt.show()
