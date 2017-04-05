import os, sys
import numpy as np
import argparse as arp
import multiprocessing as mpi

# Video & plot
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.figure as mpfig

# Mesa specifics
import mesaPlot as mp

# Define command line arguments
p = arp.ArgumentParser(prog='PvsNVideo', description='Script to generate videos from MESA profile\
                       files. It uses mesaPlot')
p.add_argument('--version', action='version', version='%(prog)s 0.1')
p.add_argument('-dir', '--folder', help='Folder with the profile*.data files', type=str,
               default='LOGS')
p.add_argument('-fn', '--filename', help='Name of the generated video', type=str,
               default='PvsNAbunMovie.mp4')
p.add_argument('-fps', help='Framerate of the generated video', type=int, default=10)
p.add_argument('-mencoder', help='Use MEncoder to create video', action='store_true', default=False)
p.add_argument('-t', '--title', help='Title of the plot', type=str, default='')
p.add_argument('-age', help='Show star age in the title', action='store_false', default=True)
p.add_argument('-mod', help='Show model number in the title', action='store_false', default=True)
p.add_argument('-s', '--silent', help='Do not print output on the terminal', action='store_true',
               default=False)
p.add_argument('-xl', '--xlabel', help='Label of the x axis', default=None)
p.add_argument('-yl', '--ylabel', help='Label of the y axis', default=None)
p.add_argument('-lim', help='Set the axis limits, both axis have the same limits', nargs=2,
               type=float)
p.add_argument('-clim', help='Set the colorbar limits', nargs=2, type=float, default=[1e-7, 1])
p.add_argument('-threads', help='Nuber of threads', type=int, default=4)
args = p.parse_args()  # parse arguments

os.system("mkdir _tmp_fold")

m = mp.MESA()  # initialize mesaPlot instance to read and plot data

# find all profiles to import with mesaPlot
m._loadProfileIndex(args.folder)
profiles = m.prof_ind['profile']

m.loadProfile(f=args.folder, prof=profiles[0], silent=True)

#def iterfun(k,i):

#iterargs=map(iterfun,)

fig1 = plt.figure(1, figsize=(14, 12))
ax = fig1.add_axes([0.2, 0.15, 0.7, 0.75])
p = mp.plot()
p._listAbun(m.prof)
p.plotAbunPAndN(m, show=False, fig=fig1, ax=ax, show_title_age=args.age, show_title_model=args.mod,
                mass_frac_rng=args.clim)
fig1.suptitle(args.title)
xb, xt = ax.get_xlim()  # xbottom,xtop
yb, yt = ax.get_ylim()  # ybottom,ytop
try:
    xmin = args.lim[0]
    xmax = args.lim[1]
except TypeError:
    xmin = -0.5
    xmax = max(xt, yt)
xaxis = ax.set_xlim(xmin, xmax)
try:
    yaxis = ax.set_ylim(args.lim[0], args.lim[1])
except TypeError:
    yaxis = ax.set_ylim(-0.5, max(xt, yt))


def _saveAbun(iterargs, mesaM=m, mesaP=p, f=args.folder, show_age=args.age, show_mod=args.mod,
              title=args.title, xaxis=xaxis, yaxis=yaxis, clim=args.clim, silent=args.silent):
    i, fig, thread_num = iterargs
    fig.clf()
    ax = fig.add_axes([0.2, 0.15, 0.7, 0.75])
    mesaM.loadProfile(prof=i, f=f, silent=silent)
    mesaP.plotAbunPAndN(m, show=False, fig=fig, ax=ax, show_title_age=show_age,
                        show_title_model=show_mod, mass_frac_rng=clim)
    fig.suptitle(title)
    ax.set_xlim(xaxis)
    ax.set_ylim(yaxis)
    ax.set_aspect('equal')
    fig.savefig('_tmp_fold/_tmp%04d' %(i))

i=profiles[0]
threads = np.arange(args.threads)
iterargs = [[i, fig1, 1]]
for k in threads[1:]:
    iterargs.append([i+k, plt.figure(k+1, figsize=(14, 12)), k+1])

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
        _saveAbun([i, fig1, 1])
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
