import os
import numpy as np
import mesaPlot as mp
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib.text as mtxt
import random

def AbunMovieLive(p,m,profile_list=None,fps=10,filename='AbunMovie.mp4',
                  xaxis='mass',xmin=None,xmax=None,y1rng=[10**-4,1.0],cmap=plt.cm.gist_ncar,
                  num_labels=4,xlabel=None,abun=None,show_burn=False,
                  ax=None,fig=None,show_title_model=True,show_title_age=True,
                  annotate_line=True,linestyle='-',y1label=r'Abundance',
                  title='Abundance profile',show_burn_labels=False,xrev=False,
                  show=True,save_video=False,verbose=False):
                
    fontBig=mpl.rcParams['font.size']-6
    fontSmall=mpl.rcParams['font.size']-12
    #metadata = dict(title='Abundance profile', artist='Matplotlib-mesaPlot',comment='')
    #writer = manimation.FFMpegWriter(fps=fps, metadata=metadata)
    if fig==None:
        fig=plt.figure(1,figsize=(10,10))
    if ax==None:
        ax=fig.add_subplot(111)
    if xlabel==None:
        xlabel=p.labels(xaxis)
    
    if profile_list==None:
        #find all profiles to import
        m._loadProfileIndex(m.log_fold)
        prof_list=m.prof_ind['model']
    else:
        prof_list=profile_list

    m.loadProfile(num=prof_list[0],silent=True)
    if abun is None:
        abun_list=p._listAbun(m.prof)
        log=''
    else:
        abun_list=abun
        log=''

    num_plots=len(abun_list)
    notes_list=range(num_plots)
    line_list=range(num_plots)
    x=m.prof.data[xaxis]
    if xmin==None:
        xmin=np.min(x)
    if xmax==None:
        xmax=np.max(x)

    colors=[cmap(i) for i in np.linspace(0.0,0.9,num_plots)]
    random.shuffle(colors)
    for el_num,elem in enumerate(abun_list):
        y=m.prof.data[elem]
        line_list[el_num], =ax.semilogy(x,y,color=colors[el_num],linestyle=linestyle,label=elem)
        if annotate_line:
            ind=np.argsort(x)
            x=x[ind]
            y=y[ind]
            xx=np.linspace(xmin,xmax,num_labels+2)[1:-1]
            yy=y[np.searchsorted(x,xx)]
            note_list=range(num_labels)
            for jj in xrange(num_labels):
                note_list[jj]=ax.annotate(elem,(xx[jj],yy[jj]),color=line_list[el_num].get_color(),fontsize=fontSmall)
            notes_list[el_num]=note_list
        else:
            ax.legend(loc='east',fontsize=fontSmall-6)

    ax.set_xlabel(xlabel,fontsize=fontBig)
    ax.set_ylabel(y1label,fontsize=fontBig)
    ax.set_title(title,loc='center',fontsize=fontBig)
    ax.set_ylim(y1rng)
    ax.set_xlim([xmin,xmax])
    if xrev:
        ax.invert_xaxis()
    if show_title_age:
       age_lab=ax.set_title('age= %.5e' % m.prof.head['star_age'],loc='left',fontsize=fontSmall)
    if show_title_model:
        mod_lab=ax.set_title('model= %d' % m.prof.head['model_number'],
                             loc='right',fontsize=fontSmall)
    def update_notes(note,x,y):
        note.set_position((x,y))
        note.set_clip_on(True)
    def update_line(line,elem,notes,x,annotate=annotate_line,xaxis=xaxis,ymin=y1rng[0]):
        #x=m.prof.data[xaxis]
        y=m.prof.data[elem]
        if np.max(y)>ymin:
            line.set_data(x,y)
            if annotate:
                ind=np.argsort(x)
                x=x[ind]
                y=y[ind]
                xx=np.linspace(xmin,xmax,num_labels+2)[1:-1]
                yy=y[np.searchsorted(x,xx)]
                map(update_notes,notes,xx,yy)

    #with writer.saving(fig, filename, len(prof_list)):
    i=0
    if save_video:
        os.system("mkdir _tmp_fold")
    for profile in prof_list:
            m.loadProfile(num=profile,silent=not(verbose))
            if show_title_age:
                age_lab.set_text('age= %.5e' % m.prof.head['star_age'])
            if show_title_model:
                mod_lab.set_text('model= %d' % m.prof.head['model_number'])
            x_list=[m.prof.data[xaxis]]*num_plots
            map(update_line,line_list,abun_list,notes_list,x_list)    
            fig.canvas.draw()
            if save_video:
                plt.savefig('_tmp_fold/_tmp%04d' % i)
                i+=1
            if show:
                plt.pause(0.001)
            #writer.grab_frame()

    if save_video:
        silence=''
        if not(verbose):
            silence = '-nostats -loglevel 0 -hide_banner '
        ffmpeg = ''.join(['ffmpeg ', silence, '-framerate %d ' %fps, 
                          '-i _tmp_fold/_tmp%04d.png ',filename])
        os.system(ffmpeg)
        os.system("rm -rf _tmp_fold")
