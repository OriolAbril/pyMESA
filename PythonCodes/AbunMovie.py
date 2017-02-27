import os, sys
import numpy as np

#Video & plot specifics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

#Mesa specifics
import mesaPlot as mp
import mesa_reader as ms

m=mp.MESA() #initialize mesaPlot instance to read and plot data

#how to step through the .data sequence
fold=ms.MesaLogDir() 
models = fold.model_numbers #get all available models from profiles.index

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Isotopic abundances evolution in a ms 1M star', artist='Matplotlib')
writer = FFMpegWriter(fps=5, metadata=metadata)

fig=plt.figure(figsize=(12,12))
ax=fig.add_axes([0.2,0.15,0.7,0.75])

with writer.saving(fig,"AbunEvolMovie.mp4",len(models)):
    for mod_no in models:
        ax.cla()
        m.loadProfile(num=mod_no)
        p=mp.plot()
        p.plotAbun(m,show=False,fig=fig,ax=ax)
        ax.set_xlim(0,1)
        writer.grab_frame()
