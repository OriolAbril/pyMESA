import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import pyMESAplotutils as pymp
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib.lines as mlines
from NuGridPy import mesa as ms
import re
from astropy import constants
import argparse as arp  # command line parsing module and help

# Parse arguments
p=arp.ArgumentParser(description='Script to plot data from nova bursts simulated with MESA, after\
                                  being postprocessed by ejecta.py')
p.add_argument('filenames', help='Name of the files to plot and compare', nargs='+')
p.add_argument('-l','--labels', help='Labels of each file', nargs='+')
args=p.parse_args()  # parse arguments

# Define invariable quantities and objects
nonmetals=['h1','h2','h3','he3','he4']
bcycler=plt.rcParams['axes.prop_cycle']
bcolors=[p['color'] for p in plt.rcParams['axes.prop_cycle']]
fcolors=['b','g','r','m','k']
linestyle=['-','--','-.',':',(0,(5, 1.5, 1, 1.5, 1, 1.5))]
fcycler=cycler(color=fcolors,linestyle=linestyle)
if not(args.labels):
    args.labels=args.filenames

# Create figures and axes
fig1=plt.figure(1)
ax1=fig1.add_subplot(111)
fig2=plt.figure(2)
ax2=fig2.add_subplot(111)
fig1bis=plt.figure(10)
ax1bis=fig1bis.add_subplot(111)
fig2bis=plt.figure(20)
ax2bis=fig2bis.add_subplot(111)
fig3=plt.figure(3)
ax3=fig3.add_subplot(111)
fig4=plt.figure(4)
ax4=fig4.add_subplot(111)
fig5=plt.figure(5)
ax5=fig5.add_axes([0.17,0.13,0.75,0.75])
fig6=plt.figure(6)
ax6=fig6.add_axes([0.17,0.13,0.75,0.75])
fig7=plt.figure(7)
ax7=fig7.add_subplot(111)

def load_ejecta_txt(name,cols):
    f=open(name+'.txt','r')
    lines=[f.readline() for i in range(4)]
    f.close()
    line=lines[0].replace(':',',')
    amasses=[int(i[1]) for i in re.findall(pym.abunPat,line)]
    abun_list=line.split(',')[1:]
    line=lines[1].replace(':',',')
    Tmax=np.array([float(i) for i in line.split(',')[1:]])
    line=lines[2].replace(':',',')
    vels=np.empty((cols,2))
    vels[:,0]=[float(i) for i in line.split(',')[1:]]
    line=lines[3].replace(':',',')
    vels[:,1]=[float(i) for i in line.split(',')[1:]]
    if abun_list[-1][-1]=='\n':
        abun_list[-1]=abun_list[-1][:-1]
    return abun_list,Tmax,vels,amasses

legf=[]
legf2=[]
for fname,flab,fcyc in zip(args.filenames,args.labels,fcycler()):
    #analyze_list=['o14','o15','o16','o17','ne20','ne22']
    fcolor=fcyc['color']
    fline=fcyc['linestyle']
    legf.append(mlines.Line2D([], [], color=fcolor, label=flab))
    legf2.append(mlines.Line2D([], [], color=fcolor, ls=fline, label=flab))
    ejected_mass=np.loadtxt(fname+'.dat')[:,:]
    shape=np.shape(ejected_mass)
    num_bursts=shape[0]
    abun_list,Tmax,vels,amasses=load_ejecta_txt(fname,shape[0])
    unstable_list=[iso for iso in abun_list if iso not in pym.stable_isos]
    stable_list=[iso for iso in abun_list if iso in pym.stable_isos]
    analyze_list=abun_list
    analyze_indexs=[abun_list.index(iso) for iso in analyze_list]
    bursts=np.arange(1,num_bursts+1)
    metallicity=np.zeros(num_bursts)
    legb=[]
    for j,bcyc in zip(xrange(num_bursts),bcycler()):
        bcolor=bcyc['color']
        legb.append(mlines.Line2D([], [], color=bcolor, label='Burst num %d' %(j+1)))
        pymp.plotAbunByA(ax1,analyze_list,ejected_mass[j,analyze_indexs],color=bcolor,ls=fline,solar=False)
        pymp.plotAbunByA(ax1bis,analyze_list,ejected_mass[j,analyze_indexs],color=fcolor,solar=False)
        #pymp.plotAbunText(ax1,abun_list,ejected_mass[j,:],amasses,color=colors[j],solar=False)
        pymp.plotAbunByA(ax2,analyze_list,ejected_mass[j,analyze_indexs],color=bcolor,ls=fline,solar=True)
        pymp.plotAbunByA(ax2bis,analyze_list,ejected_mass[j,analyze_indexs],color=fcolor,solar=True)
        #pymp.plotAbunText(ax2,abun_list,ejected_mass[j,:],amasses,color=colors[j],solar=True)
        total=0
        for i,iso in enumerate(abun_list):
            if iso not in nonmetals:
                metallicity[j]+=ejected_mass[j,i]
                total+=ejected_mass[j,i]
            else:
                total+=ejected_mass[j,i]
        if not np.isclose(total,1.):
            print 'Warning! Sum of mass fractions equals %f' %total
    for iso in analyze_list:
        i=abun_list.index(iso)
        mean=np.mean(ejected_mass[:,i])
        if mean>1e-15:
            ax3.plot(bursts,ejected_mass[:,i],label=iso)
            ax3.text(bursts[-1],ejected_mass[-1,i],iso)
            ax3.text(bursts[0],ejected_mass[0,i],iso)
            ax4.plot(bursts,ejected_mass[:,i]/ejected_mass[0,i],label=iso)
            ax4.text(bursts[-1],ejected_mass[-1,i]/ejected_mass[0,i],iso)

    ax5.plot(bursts,Tmax,'o-',label=flab,color=fcolor)
    ax6.plot(bursts,metallicity,'o-',linewidth=1,markersize=2.5,label=flab,color=fcolor)
    ax7.plot(bursts,vels[:,0],'o-',label=flab+' $v_{max}$')
    ax7.plot(bursts,vels[:,1],'o-',label=flab+' $v_{min}$')

# Customize plots
ax1.legend(handles=legb)
ax1.grid(True)
ax1.set_title('Chemical composition of the ejected material')
ax2.legend(handles=legb)
ax2.grid(True)
ax2.set_title('Chemical composition of the ejected material compared to solar abundances')
ax1bis.legend(handles=legf)
ax1bis.grid(True)
ax1bis.set_title('Chemical composition of the ejected material')
ax2bis.legend(handles=legf)
ax2bis.grid(True)
ax2bis.set_title('Chemical composition of the ejected material compared to solar abundances')
ax3.set_yscale('log')
ax3.legend()
ax3.set_xlabel('Burst number')
ax3.set_ylabel('Ejected mass fraction')
ax3.grid(True)
#ax3.set_title('Ejected mass')
ax4.set_yscale('log')
#ax4.legend()
ax4.set_xlabel('Burst number')
ax4.set_ylabel('Ejected mass fraction relative to 1st burst')
ax4.grid(True)
#ax4.set_title('Ejected mass')
ax5.grid(True)
ax5.legend()
ax5.set_xlabel('Burst number')
ax5.set_ylabel('$\log(T_{max})$ (K)')
#ax5.set_title('')
ax6.set_xlabel('Burst number')
ax6.set_ylabel('Metallicity')
ax6.grid(True)
ax6.legend()
ax7.legend()
ax7.set_yscale('log')
ax7.grid(True)
ax7.legend()
ax7.set_xlabel('Burst number')
ax7.set_ylabel('Ejected cell velocity (m/s)')
plt.show()
