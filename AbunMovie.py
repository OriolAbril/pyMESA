import os, sys
import argparse as arp

#Video & plot specifics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

#Mesa specifics
import mesaPlot as mp

p=arp.ArgumentParser(prog='AbunVideo',description='Script to generate videos from MESA profile files. It uses mesaPlot')
p.add_argument('--version',action='version',version='%(prog)s 0.0')
p.add_argument('-t','--title',help='Title of the plot',default=None)
p.add_argument('-age',help='Show star age in the title',action='store_true',default=False)
p.add_argument('-xn','--xname',help='Name of the column to be used as x data',type=str,default='mass')
p.add_argument('-xl','--xlabel',help='Label of the x axis',default=None)
p.add_argument('-yl','--ylabel',help='Label of the y axis',default=None)
p.add_argument('-xlim',help='Set the xaxis limits',nargs=2,type=float)
args=p.parse_args() #parse arguments

if args.xlim:
    xmin=args.xlim[0]
    xmax=args.xlim[1]
else:
    xmin=None
    xmax=None

m=mp.MESA() #initialize mesaPlot instance to read and plot data

#find all profiles to import with mesaPlot
m._loadProfileIndex('LOGS')
models=m.prof_ind['model']

try:
    m.loadProfile(num=models[0],silent=True)
    x=m.prof.data[args.xname]
    if not(args.xlim):
        xmin=min(x)
        xmax=max(x)
except (KeyError,AttributeError):
    raise ValueError(args.xname+"not found as data name")

fig=plt.figure(figsize=(12,12))
ax=fig.add_axes([0.2,0.15,0.7,0.75])
p=mp.plot()
invert=False
try:
    p.plotAbun(m,show=False,fig=fig,ax=ax,xaxis=args.xname,xmin=xmin,xmax=xmax,show_title_age=args.age,ylabel=args.ylabel,title=args.title,xlabel=args.xlabel)
except ValueError:
    aux=xmax
    xmax=xmin
    xmin=aux
    print xmin,xmax
    p.plotAbun(m,show=False,fig=fig,ax=ax,xaxis=args.xname,xmin=xmin,xmax=xmax,show_title_age=args.age,ylabel=args.ylabel,title=args.title,xlabel=args.xlabel)
    ax.invert_xaxis()

xaxlim=ax.get_xlim()
yaxlim=ax.get_ylim()
axratio=ax.get_aspect()

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Isotopic abundances evolution in a ms 1M star', artist='Matplotlib')
writer = FFMpegWriter(fps=5, metadata=metadata)
with writer.saving(fig,"AbunEvolMovie.mp4",len(models)):
    for mod_no in models:
        ax.cla()
        m.loadProfile(num=mod_no)
        p=mp.plot()
        p.plotAbun(m,show=False,fig=fig,ax=ax,xaxis=args.xname,xmin=xmin,xmax=xmax,show_title_age=args.age,ylabel=args.ylabel,title=args.title,xlabel=args.xlabel)
        ax.set_xlim(xaxlim)
        ax.set_ylim(yaxlim)
        ax.set_aspect(axratio)
        writer.grab_frame()
