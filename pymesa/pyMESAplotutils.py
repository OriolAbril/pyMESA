import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym

def plotAbunByA(ax,isos_list,ejected_mass,color=None,ls=None,solar=False,labels=True):
# create dictionary containing the isotopes for each element
    eldict={}
    amasses=range(len(isos_list))
    for i,iso in enumerate(isos_list):
        m=pym.abunPat.match(iso)
        amasses[i]=int(m.groups(1)[1])
        el=m.groups(1)[0]
        try:
            eldict[el]+=[iso]
        except KeyError:
            eldict[el]=[iso]
    for el in eldict:
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
        line, =ax.plot(masses, ej_iso, 'o-', color=color, linewidth=0.5, markersize=1, linestyle=ls)
        if labels:
            try:
                ytextval=np.max(ej_iso)
                xtextval=masses[ej_iso.index(ytextval)]
                ax.text(xtextval,ytextval,el.title(),color=color,clip_on=True)
            except ValueError:
                pass
    ax.set_yscale('log')
    ax.set_xlim([0, max(amasses)+2])
    ax.set_xlabel('Atomic mass number')
    if solar:
        ax.set_ylim([1e-10, 1e3])
        ax.set_ylabel('Mass fraction/Solar mass fraction')
    else:
        ax.set_ylim([1e-10, 1.5])
        ax.set_ylabel('Mass fraction')

def plotAbunText(ax,isos_list,ejected_mass,amasses,color=None,solar=False):
    for i,iso in enumerate(isos_list):
        if solar:
            if iso in pym.stable_isos:
                solar=pym.sol_comp_ag89[pym.stable_isos.index(iso)]
                ax.text(amasses[i], ejected_mass[i]/solar, iso, color=colors[j], clip_on=True)
        else:
            ax.text(amasses[i], ejected_mass[i], iso, color=colors[j], clip_on=True)
    ax.set_yscale('log')
    ax.set_xlim([0, max(amasses)+1])
    ax.set_xlabel('Atomic mass number')
    if solar:
        ax.set_ylim([1e-10, 1e3])
        ax.set_ylabel('Mass fraction/Solar mass fraction')
    else:
        ax.set_ylim([1e-10, 1.5])
        ax.set_ylabel('Mass fraction')
