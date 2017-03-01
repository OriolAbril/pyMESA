import os, sys
import numpy as np

#Video & plot 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

#Mesa specifics
import mesaPlot as mp
#import mesa_reader as ms

m=mp.MESA() #initialize mesaPlot instance to read and plot data

#find all profiles to import with mesa_reader
#fold=ms.MesaLogDir() 
#models = fold.model_numbers #get all available models from profiles.index

#find all profiles to import with mesaPlot
m._loadProfileIndex('LOGS')
models=m.prof_ind['model']

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Isotopic abundances evolution in a ms 1M star', artist='Matplotlib')
writer = FFMpegWriter(fps=5, metadata=metadata)


fig=plt.figure(figsize=(14,12))
with writer.saving(fig,"PvsNAbunMovie.mp4",len(models)):
    for mod_no in models:
        ax=fig.add_axes([0.2,0.15,0.7,0.75])
        m.loadProfile(num=mod_no)
        p=mp.plot()
        p.plotAbunPAndN(m,show=False,fig=fig,ax=ax)
        xb,xt=ax.get_xlim() #xbottom,xtop
        yb,yt=ax.get_ylim() #ybottom,ytop
        ax.set_xlim(-0.5,max(xt,yt))
        ax.set_ylim(-0.5,max(xt,yt))
        ax.set_aspect('equal')
        writer.grab_frame()
        fig.clf()
