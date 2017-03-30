import os, sys
import argparse as arp

#Video & plot specifics
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

#Mesa specifics
import mesaPlot as mp

p=arp.ArgumentParser(prog='AbunVideo',description='Script to generate videos from MESA profile files. It uses mesaPlot')
p.add_argument('--version',action='version',version='%(prog)s 0.1')
par = arp.ArgumentParser(add_help=False,conflict_handler='resolve')
par.add_argument('-t','--title',help='Title of the plot',default='',type=str)
par.add_argument('-fn','--filename',help='Name of the .mp4 created file',default='AbunMovie.mp4',type=str)
par.add_argument('-age',help='Show star age in the title',action='store_true',default=False)
par.add_argument('-xlim',help='Set the xaxis limits',nargs=2,type=float)
par.add_argument('-ylim',help='Set the yaxis limits',nargs=2,type=float,default=[10**-3,1.0])
mpar = arp.ArgumentParser(add_help=False,conflict_handler='resolve')
mpar.add_argument('-xn','--xname',help='Name of the column to be used as x data',type=str,default='mass')
mpar.add_argument('-xl','--xlabel',help='Label of the x axis',default=None)
subp = p.add_subparsers()
n = subp.add_parser('simp',help='Abundance profile',parents=[par,mpar])
n.set_defaults(which='abun')
a = subp.add_parser('byA',help='Abundance of elements with atomic mass on the X axis',parents=[par])
a.set_defaults(which='byA')
s = subp.add_parser('byA-s',help='Abundance of elements with atomic mass on the X axis, normalized to solar values',parents=[par])
s.set_defaults(which='byA-s')
args=p.parse_args() #parse arguments

m=mp.MESA()

#find all profiles to import with mesaPlot
m._loadProfileIndex('LOGS')
models=m.prof_ind['model']

if args.xlim:
    xmin=args.xlim[0]
    xmax=args.xlim[1]
else:
    xmin=None
    xmax=None

m.loadProfile(num=models[0],silent=True)
if args.which=='abun':
    try:
        x=m.prof.data[args.xname]
    except (KeyError,AttributeError):
        raise ValueError(args.xname+"not found as data name")

fig=plt.figure(figsize=(12,12))
ax=fig.add_axes([0.2,0.15,0.7,0.75])
p=mp.plot()
invert=False
if args.which=='abun':
    p.plotAbun(m,show=False,fig=fig,ax=ax,xaxis=args.xname,xmin=xmin,xmax=xmax,show_title_age=args.age,
            xlabel=args.xlabel,y1rng=args.ylim)
elif args.which=='byA':
    p.plotAbunByA(m,show=False,fig=fig,ax=ax,show_title_age=args.age,yrng=args.ylim)
else:
    p.set_solar('ag89')
    p.plotAbunByA_Stable(m,show=False,fig=fig,ax=ax,show_title_age=args.age,yrng=args.ylim)
fig.suptitle(args.title)
xaxlim=ax.get_xlim()
yaxlim=ax.get_ylim()
axratio=ax.get_aspect()

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Isotopic abundances evolution'+args.title, artist='AbunVideo - Matplotlib')
writer = FFMpegWriter(fps=10, metadata=metadata)
with writer.saving(fig,"movie.mp4",len(models)):
    for mod_no in models:
        ax.cla()
        m.loadProfile(num=mod_no)
        p=mp.plot()
        if args.which=='abun':
            p.plotAbun(m,show=False,fig=fig,ax=ax,xaxis=args.xname,xmin=xmin,xmax=xmax,show_title_age=args.age,
                    xlabel=args.xlabel,y1rng=args.ylim)
        elif args.which=='byA':
            p.plotAbunByA(m,show=False,fig=fig,ax=ax,show_title_age=args.age,yrng=args.ylim)
        else:
            p.set_solar('ag89')
            p.plotAbunByA_Stable(m,show=False,fig=fig,ax=ax,show_title_age=args.age,yrng=args.ylim)
        ax.set_xlim(xaxlim)
        ax.set_ylim(yaxlim)
        ax.set_aspect(axratio)
        writer.grab_frame()
