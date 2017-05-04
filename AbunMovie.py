import os, sys
import numpy as np
import argparse as arp
import multiprocessing as mpi
import re

# Video & plot
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.figure as mpfig

# Mesa specifics
import mesaPlot as mp

abunPat = re.compile('([a-z]{1,3})[0-9]{1,3}',re.IGNORECASE)
def _getAbun(m,p,abunPat=abunPat):
    abundances = []
    for data_name in m.prof.data_names:
        abunMatch = abunPat.match(data_name)
        if abunMatch:
            elem_name = abunMatch.groups(1)[0]
            if elem_name in p.elements:
                abundances.append(data_name)
    return abundances

# Define command line arguments
p = arp.ArgumentParser(prog='AbunVideo', description='Script to generate videos from MESA profile\
                     files. It uses mesaPlot')
p.add_argument('--version', action='version', version='%(prog)s 0.1')
p.add_argument('-fn', '--filename', help='Name of the .mp4 created file', type=str)
p.add_argument('-fps', help='Framerate of the generated video', type=int, default=10)
p.add_argument('-mencoder', help='Use MEncoder to create video', action='store_true', default=False)
p.add_argument('-dir', '--folder', help='Folder with the profile*.data files', type=str,
               default='LOGS')
p.add_argument('-threads', help='Nuber of threads', type=int, default=4)
par = arp.ArgumentParser(add_help=False, conflict_handler='resolve')
par.add_argument('-age', help='Show star age in the title', action='store_false', default=True)
par.add_argument('-mod', help='Show model number in the title', action='store_false', default=True)
par.add_argument('-s', '--silent', help='Do not print output on the terminal', action='store_true',
               default=False)
par.add_argument('-t', '--title', help='Title of the plot', default='', type=str)
par.add_argument('-xlim', help='Set the xaxis limits', nargs=2, type=float)
par.add_argument('-ylim', help='Set the yaxis limits', nargs=2, type=float)
mpar = arp.ArgumentParser(add_help=False, conflict_handler='resolve')
mpar.add_argument('-xn', '--xname', help='Name of the column to be used as x data', type=str,
                  default='mass')
mpar.add_argument('-xl', '--xlabel', help='Label of the x axis', default=None)
subp = p.add_subparsers()
n = subp.add_parser('prof', help='Abundance profile', parents=[par, mpar])
n.set_defaults(which='abun', ylim=[1e-4, 1.5], filename='AbunMovie.mp4')
a = subp.add_parser('byA', help='Abundance of elements with atomic mass on the X axis', 
                    parents=[par])
a.set_defaults(which='byA', filename='AbunMovieByA.mp4', ylim=[1e-15, 1.5])
s = subp.add_parser('byA-s', help='Abundance of elements with atomic mass on the X axis, normalized\
        to solar values', parents=[par])
s.set_defaults(which='byA-s', filename='AbunMovieByA-S.mp4', ylim=[1e-2, 1e2])
args = p.parse_args()  # parse arguments

os.system("mkdir _tmp_fold")
m = mp.MESA()  # initialize mesaPlot instance to read and plot data

# find all profiles to import with mesaPlot
m._loadProfileIndex(args.folder)
profiles = m.prof_ind['profile']

m.loadProfile(f=args.folder, prof=profiles[0], silent=True)
if args.which=='abun':
    try:
        x=m.prof.data[args.xname]
    except (KeyError, AttributeError):
        raise ValueError(args.xname+"not found as data name")

fig1 = plt.figure(1, figsize=(14, 12))
ax1 = fig1.add_axes([0.2, 0.15, 0.7, 0.75])
p = mp.plot()
p._listAbun(m.prof)
if args.which == 'abun':
    p.plotAbun(m, show=False, fig=fig1, ax=ax1, show_title_age=args.age, show_title_model=args.mod,
           y1rng=args.ylim, xaxis=args.xname)
elif args.which=='byA':
    abun=_getAbun(m,p)
    p.plotAbunByA(m, show=False, fig=fig1, ax=ax1, show_title_age=args.age, yrng=args.ylim,
                  show_title_model=args.mod,abun=abun)
else:
    p.set_solar('ag89')
    abundances=_getAbun(m,p)
    p.plotAbunByA(m, show=False, fig=fig1, ax=ax1, show_title_age=args.age, yrng=args.ylim,
                  show_title_model=args.mod, stable=True, abun=abundances)
fig1.suptitle(args.title)
try:
    xmin = args.xlim[0]
    xmax = args.xlim[1]
    ax1.set_xlim(xmin, xmax)
except TypeError:
    pass
try:
    ymin = args.ylim[0]
    ymax = args.ylim[1]
    ax1.set_ylim(ymin, ymax)
except TypeError:
    pass

xaxis = ax1.get_xlim()
yaxis = ax1.get_ylim()

if args.which == 'abun':
    def _saveAbun(iterargs, mesaM=m, mesaP=p, f=args.folder, show_age=args.age, show_mod=args.mod,
                  title=args.title, xlim=xaxis, ylim=yaxis, xaxis=args.xname, silent=args.silent):
        i, fig, ax, thread_num = iterargs
        ax.cla()
        mesaM.loadProfile(prof=i, f=f, silent=silent)
        mesaP.plotAbun(m, show=False, fig=fig, ax=ax, show_title_age=show_age,
                       show_title_model=show_mod, xaxis=xaxis)
        fig.suptitle(title)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        fig.savefig('_tmp_fold/_tmp%04d' %(i))
elif args.which == 'byA':
    def _saveAbun(iterargs, mesaM=m, mesaP=p, f=args.folder, show_age=args.age, show_mod=args.mod,
                  title=args.title, xlim=xaxis, ylim=yaxis, silent=args.silent):
        i, fig, ax, thread_num = iterargs
        ax.cla()
        mesaM.loadProfile(prof=i, f=f, silent=silent)
        mesaP.plotAbunByA(m, show=False, fig=fig, ax=ax, show_title_age=show_age,
                          show_title_model=show_mod)
        fig.suptitle(title)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        fig.savefig('_tmp_fold/_tmp%04d' %(i)) 
else:
    def _saveAbun(iterargs, mesaM=m, mesaP=p, f=args.folder, show_age=args.age, show_mod=args.mod,
                  title=args.title, xlim=xaxis, ylim=yaxis, silent=args.silent):
        i, fig, ax, thread_num = iterargs
        ax.cla()
        mesaM.loadProfile(prof=i, f=f, silent=silent)
        p.set_solar('ag89')
        mesaP.plotAbunByA(m, show=False, fig=fig, ax=ax, show_title_age=show_age,
                          show_title_model=show_mod, stable=True)
        fig.suptitle(title)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        fig.savefig('_tmp_fold/_tmp%04d' %(i))

i=profiles[0]
threads = np.arange(args.threads)
iterargs = [[i, fig1, ax1, 1]]
for k in threads[1:]:
    fig = plt.figure(k+1, figsize=(14, 12))
    ax = fig.add_axes([0.2, 0.15, 0.7, 0.75])
    iterargs.append([i+k, fig, ax, k+1])

def abunIter(i, threads=threads, iterargs=iterargs):
    for k in threads:
        iterargs[k][0] = i+k
    pool = mpi.Pool(processes=args.threads)
    pool.map(_saveAbun, iterargs)
    pool.close()
    pool.join()
    i += args.threads

map(abunIter, profiles[:-args.threads:args.threads])
residual=len(profiles) % args.threads

for i in profiles[-residual:]:
    try:
        _saveAbun([i, fig1, ax1, 1])
    except IndexError:
        break

if args.mencoder:
    os.system("opt='vbitrate=2160000:mbd=2:keyint=132:v4mv:vqmin=3:vlelim=-4:vcelim=7:\
          lumi_mask=0.07:dark_mask=0.10:naq:vqcomp=0.7:vqblur=0.2:mpeg_quant'")
    os.system("mencoder 'mf://_tmp_fold/_tmp*.png' -mf type=png:fps=%d \
          -ovc lavc -lavcopts vcodec=mpeg4:vpass=1:$opt -oac copy -o %s" %(args.fps, args.filename))
else: 
    silence=''
    if args.silent:
        silence = '-nostats -loglevel 0 -hide_banner '
    ffmpeg = ''.join(['ffmpeg ', silence, '-framerate %d ' %args.fps, '-i _tmp_fold/_tmp%04d.png ',
                      args.filename])
    os.system(ffmpeg)
os.system("rm -rf _tmp_fold")
