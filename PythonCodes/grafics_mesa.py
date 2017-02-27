#import libraries
import argparse as arp #command line parsing module and help
import numpy as np 
import mesa_reader as msr
import re #regular expressions

p=arp.ArgumentParser(prog='MESA_grafics',description='Script to plot data from the .data output files from MESA')
p.add_argument('--version',action='version',version='%(prog)s 0.2')
p.add_argument('files',metavar='FILES',help='Name of the .data type file/s with the extension',nargs='+')
group=p.add_mutually_exclusive_group(required=True)
group.add_argument('-hd','--headers',help='Show available headers in the files. Default: False',action='store_true',default=False)
group.add_argument('-c','--columns',help='Columns to be plotted, the first one will be used as x values. The separation between column  mes for the same file should be a comma and between different files a space.',nargs='+')
p.add_argument('-s','--separator',help='Separator character/s or regular expression to match the separator',type=str,default=r'\s+')
pltpar=p.add_argument_group(title='Commands to personalize plots')
pltpar.add_argument('-mp',help='Do not show plot with matplotlib. Default: True',action='store_false',default=True)
pltpar.add_argument('-off','--offset',help='Use matplotlib''s default offest in y axis. Default: False',action='store_false',default=True)
pltpar.add_argument('-eps',help='Write plot as an Encapsulated PostScript. The name can be specified',type=str,nargs='?',default='noeps',const='sieps')
pltpar.add_argument('-sc','--scale',help='Choose the scale between: liner, semilogy, semilogx or logxy',type=str,choices=['lin','logy','logx','loglog','logxy'])
pltpar.add_argument('-co','--colors',help='Colors to be used in the plot, they must be valid matplotlib colors',nargs='+')
pltpar.add_argument('-l','--legend',help='Labels for the legend. Default text is name of file without extension',nargs='+')
pltpar.add_argument('-t','--title',help='Title of the plot',type=str,default='')
pltpar.add_argument('-lt','--legtit',help='Title for the legend',type=str,default='')
pltpar.add_argument('-xl','--xlabel',help='Label of the x axis',type=str,default='')
pltpar.add_argument('-yl','--ylabel',help='Label of the y axis',type=str,default='')
pltpar.add_argument('-x','--xaxis',help='Set the xaxis limits',nargs=2,type=float)
pltpar.add_argument('-y','--yaxis',help='Set the yaxis limits',nargs=2,type=float)
args=p.parse_args() #parse arguments

if not(args.headers): #set plot variables and configuration
    if args.scale=='loglog':
        args.scale='logxy'
    l1=len(args.files)
    colo=['blue','black','red','green','yellow','cyan','magenta']*3 #set default colors
    colus=args.columns
    if args.colors: #if flag -co present, overwrite default colors
        for colnum,col in enumerate(args.colors):
            colo[colnum]=col

    if (args.mp or args.eps!='noeps'): #import and initialize plot
        import matplotlib.font_manager as fnt
        import matplotlib.pyplot as plt
        if args.offset:
            import matplotlib.ticker as tk
            marques=tk.ScalarFormatter(useOffset=False)
        xlab=args.xlabel
        fig=plt.figure(1)
        graf=fig.add_axes([0.13,0.1, 0.8, 0.8])

colcount=0
legcount=0 #legend label counter
fpat=re.compile(r'(?P<nom>[^/\.]+)\.') #regular expression to obtain the name of the file without extension
for filecount,doc in enumerate(args.files): #loop over each file
    fd=open(doc,'r')
    h=msr.MesaData(doc)
    if args.headers: #print headers
        print doc
        for name1,name2,name3 in zip(h.bulk_names[::3],h.bulk_names[1::3],h.bulk_names[2::3]):
            print '{:<30}{:<30}{:<}'.format(name1,name2,name3)
        print '\n'
    else: 
        docols=[col for col in re.split(',',colus[filecount])] #get number of plots
        numplots=len(docols)-1
        if args.legend: #check legend labels
            leg=args.legend[legcount:numplots]
            legcount+=numplots
        else: #if unexistent, set legend labels to corresponent header
            leg=['']*numplots
            for numpl,pl in enumerate(docols[1:]):
                leg[numpl]=pl
        x=h.data(docols[0]) #set x values to first parsed column 
        if (args.mp or args.eps!='noeps'):
            for i in range(numplots):
                y=h.data(docols[i+1])
                graf.plot(x,y,color=colo[colcount],label=leg[i])
                colcount+=1
if not(args.headers):
    if (args.mp or args.eps!='noeps'):
        #set axis labels and limits
        graf.set_xlabel(args.xlabel)
        graf.set_ylabel(args.ylabel)
        if args.yaxis: 
            graf.set_ylim(args.yaxis)
        if args.xaxis:
            graf.set_xlim(args.xaxis)
        if args.offset:
            graf.yaxis.set_major_formatter(marques) #set y axis marker format
        #set axis scale
        if (args.scale=='logx' or args.scale=='logxy'):
            graf.set_xscale('log')
        if (args.scale=='logy' or args.scale=='logxy'):
            graf.set_yscale('log')
        #set title, grid and legend
        fig.suptitle(args.title)
        graf.grid(True)
        graf.legend(loc='best', prop=fnt.FontProperties(size='medium'),title=args.legtit)
    if args.eps!='noeps': #save figure
        if args.eps!='sieps': #save figure with specified name, extension is checked
            seed=fpat.search(args.eps) 
            if seed:
                figname=seed.group('nom')+'.eps' 
            else:
                figname=args.eps+'.eps' 
        else: #set figure name to input file name
            seed=fpat.search(args.files[0])
            if seed:
                figname=seed.group('nom')+'.eps'
            else:
                figname=args.files[0]+'.eps'
        fig.savefig(figname, format='eps', dpi=1000)
    if args.mp:    
        plt.show() #show figure
