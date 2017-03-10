import os, sys
import numpy as np
import argparse as arp

#Video & plot 
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.cm as cm

#Mesa specifics
import mesaPlot as mp

p=arp.ArgumentParser(prog='PvsNVideo',description='Script to generate videos from MESA profile files. It uses mesaPlot')
p.add_argument('--version',action='version',version='%(prog)s 0.0')
p.add_argument('-t','--title',help='Title of the plot',type=str,default='')
p.add_argument('-age',help='Show star age in the title',action='store_true',default=False)
p.add_argument('-xn','--xname',help='Name of the column to be used as x data',type=str,default='mass')
p.add_argument('-xl','--xlabel',help='Label of the x axis',default=None)
p.add_argument('-yl','--ylabel',help='Label of the y axis',default=None)
p.add_argument('-lim',help='Set the axis limits, both axis have the same limits',nargs=2,type=float)
p.add_argument('-clim',help='Set the colorbar limits',nargs=2,type=float)
args=p.parse_args() #parse arguments

if args.clim:
    cmin=args.clim[0]
    cmax=args.clim[1]
else:
    cmin=-5
    cmax=0


m=mp.MESA() #initialize mesaPlot instance to read and plot data

#find all profiles to import with mesaPlot
m._loadProfileIndex('LOGS')
models=m.prof_ind['model']

try:
    m.loadProfile(num=models[0],silent=True)
    x=m.prof.data[args.xname]
except (KeyError,AttributeError):
    raise ValueError(args.xname+"not found as data name")

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Isotopic abundances evolution in a ms 1M star', artist='Matplotlib')
writer = FFMpegWriter(fps=5, metadata=metadata)


fig=plt.figure(figsize=(14,12))
ax=fig.add_axes([0.2,0.15,0.7,0.75])
p=mp.plot()
p._listAbun(m.prof)
p.plotAbunPAndN(m,show=False,fig=fig,ax=ax,show_title_age=args.age)
xb,xt=ax.get_xlim() #xbottom,xtop
yb,yt=ax.get_ylim() #ybottom,ytop
if args.lim:
    xaxis=ax.set_xlim(amin,amax)
    yaxis=ax.set_ylim(amin,amax)
else:
    xaxis=ax.set_xlim(-0.5,max(xt,yt))
    yaxis=ax.set_ylim(-0.5,max(xt,yt))
cb=plt.get_cmap()
cbar=cm.ScalarMappable(cmap=cb)
clim=cbar.set_clim(vmin=cmin,vmax=cmax)

with writer.saving(fig,"PvsNAbunMovie.mp4",len(models)):
    for mod_no in models:
        fig.clf()
        ax=fig.add_axes([0.2,0.15,0.7,0.75])
        m.loadProfile(num=mod_no)
        p=mp.plot()
        p.plotAbunPAndN(m,show=False,fig=fig,ax=ax,show_title_age=args.age)
        fig.suptitle(args.title)
        ax.set_xlim(xaxis)
        ax.set_ylim(yaxis)
        ax.set_aspect('equal')
        cb=cm.get_cmap()
        cbar=cm.ScalarMappable(cmap=cb)
        clim=cbar.set_clim(vmin=cmin,vmax=cmax)
        writer.grab_frame()
