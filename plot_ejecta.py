import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from NuGridPy import mesa as ms
import re
from astropy import constants
import argparse as arp  # command line parsing module and help

p=arp.ArgumentParser(description='Script to save and plot data from nova bursts simulated with MESA')
p.add_argument('filename', help='Name of the files to save')
args=p.parse_args()  # parse arguments

colors=[p['color'] for p in plt.rcParams['axes.prop_cycle']]
ejected_mass=np.loadtxt(args.filename+'.dat')[:,:]
f=open(args.filename+'.txt','r')
line=f.readline()
f.close()
line=line.replace(':',',')
abun_list=line.split(',')[1:]
abunPat=re.compile(r'([a-z]{1,3})([0-9]{1,3})',re.IGNORECASE)
amasses=[int(i[1]) for i in re.findall(abunPat,line)]
shape=np.shape(ejected_mass)
bursts=np.arange(1,shape[0]+1)
leg=[]
plt.figure(1)
for j in xrange(shape[0]):
    leg.append(mlines.Line2D([], [], color=colors[j], label='Burst num %d' %(j+1)))
    for i,iso in enumerate(abun_list):
        plt.text(amasses[i], ejected_mass[j,i],iso,color=colors[j],clip_on=True)
plt.yscale('log')
plt.axis([0, max(amasses)+1, 1e-10, 1.5])
plt.legend(handles=leg)

plt.figure(2)
for j in xrange(shape[0]):
    for i,iso in enumerate(abun_list):
        if iso in pym.stable_isos:
            solar=pym.sol_comp_ag89[pym.stable_isos.index(iso)]
            plt.text(amasses[i], ejected_mass[j,i]/solar, iso, color=colors[j], clip_on=True)
plt.yscale('log')
plt.axis([0, max(amasses)+3, 1e-1, 1e4])
plt.legend(loc='upper left',handles=leg)

analyze_list=['li7','o15','o16','o17','ne20','ne22']
plt.figure(3)
for iso in analyze_list:
    i=abun_list.index(iso)
    mean=np.mean(ejected_mass[:,i])
    if mean>1e-15:
        plt.plot(bursts,ejected_mass[:,i]-ejected_mass[0,i],label=iso)
plt.legend()
#plt.axis([0,10,0.05,50])
plt.show()
