# import libraries
import argparse as arp  # command line parsing module and help
import numpy as np 
import pandas as pd
import re  # regular expressions
import sys,os
scriptpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptpath)
import pymesa.tools as pym
import pymesa.plot_tools as pymp

class matplotlibScale(arp.Action):
    def __init__(self,
                 option_strings,
                 dest,
                 nargs=None,
                 const=None,
                 default=None,
                 type=None,
                 choices=None,
                 required=False,
                 help=None,
                 metavar=None):
        arp.Action.__init__(self,
                                 option_strings=option_strings,
                                 dest=dest,
                                 nargs=nargs,
                                 const=const,
                                 default=default,
                                 type=type,
                                 choices=choices,
                                 required=required,
                                 help=help,
                                 metavar=metavar)

    def __call__(self, parser, namespace, value, option_string=None):
        yscale = 'log' if value in ['logy','loglog','logxy'] else 'linear'
        xscale = 'log' if value in ['logx','loglog','logxy'] else 'linear'
        # Save the results in the namespace using the destination
        # variable given to our constructor.
        setattr(namespace, 'yscale', yscale)
        setattr(namespace, 'xscale', xscale)
        delattr(namespace, 'scale')

p=arp.ArgumentParser(prog='MESA_grafics',description='Script to plot data from the .data output files from MESA')
p.add_argument('--version', action='version', version='%(prog)s 1.0')
p.add_argument('files', metavar='FILES', help='Name of the .data type file/s with the extension', nargs='+')
group=p.add_mutually_exclusive_group(required=True)
group.add_argument('-c', '--columns', help='Columns to be plotted, the first one will be used as x values.\
                   The separation between columnes for the same file should be a comma and between different\
                   files a space.', nargs='+')
group.add_argument('-hd', '--headers', help='Show available headers in the files. Default: False', 
                   action='store_true', default=False)
hdpar=p.add_argument_group(title='Commands to personalize the headers output')
hdpar.add_argument('-tc', '--terminalcols', help='Number of columns to show the headers when using the -hd flag', 
                   type=int, default=0)
hdpar.add_argument('-o', '--order', help='Choose fist direction to sort the names, either first descending and\
                   then to the right (default) or viceversa', type=str, default='descending', 
                   choices=['d', 'descending', 'r', 'right'])
pltpar=p.add_argument_group(title='Commands to personalize plots')
pltpar.add_argument('-pqg', help='Use PyQtGraph as plotting module instead of Matplotlib', action='store_true',
                    default=False)
pltpar.add_argument('-np', help='Do not show the plot. Default: False', action='store_true', default=False)
pltpar.add_argument('-off', '--offset', help='Use matplotlib''s default offest in axis ticks. Default:False', 
                    action='store_true', default=False)
pltpar.add_argument('-eps', help='Write matplotlib plot as an Encapsulated PostScript. The name can be specified',
                    type=str, nargs='?', default='noeps', const='sieps')
pltpar.add_argument('-sc', '--scale', help='Choose the scale between: liner, semilogy, semilogx or logxy',
                    type=str, default='lin', choices=['lin', 'logy', 'logx', 'loglog', 'logxy'], action=matplotlibScale)
pltpar.add_argument('-co', '--colors', help='Colors to be used in the plot, they must be valid matplotlib colors',
                    nargs='+')
pltpar.add_argument('-lw', '--linewidth', help='Set linewidth of matplotlib plots', default=1,
                    type=float)
pltpar.add_argument('-t', '--title', help='Title of the plot', type=str, default='')
pltpar.add_argument('-lt', '--legtit', help='Title for the legend', type=str, default='')
pltpar.add_argument('-l', '--legend', help='Labels for the legend. Default text is name of y data column.',
                    nargs='+')
pltpar.add_argument('-lp', '--legprefix', help='Prefix for the legend labels. If present, legprefix must\
                    have the same length as files and legend as the number of columns minus one',nargs='+')
pltpar.add_argument('-xl', '--xlabel', help='Label of the x axis', type=str)
pltpar.add_argument('-yl', '--ylabel', help='Label of the y axis', type=str, default='')
pltpar.add_argument('-x', '--xlim', help='Set the xaxis limits', nargs=2, type=float)
pltpar.add_argument('-y', '--ylim', help='Set the yaxis limits', nargs=2, type=float)
args=p.parse_args()  # parse arguments

if args.headers: # set variables for header mode
    args.order= 'descending' if args.order[0]=='d' else 'right'
    args.terminalcols= 'auto' if args.terminalcols==0 else args.terminalcols

else: # set plot variables and configuration
    try:
        args.xscale
    except AttributeError:
        setattr(args, 'xscale', 'lin')
        setattr(args, 'yscale', 'lin')
    if len(args.files)!=len(args.columns):
        args.columns=[args.columns[0]]*len(args.files)
    allplots = sum([len(k.split(','))-1 for k in args.columns])
    if not(args.xlabel):
        args.xlabel=args.columns[0].split(',')[0]
    if args.legprefix:
        y_columns = args.columns[0].split(',')[1:]
        if (len(args.files)==len(args.legprefix) and not args.legend):
            args.legend=[pre+lab for pre in args.legprefix for lab in y_columns]
        elif len(args.legend)==len(y_columns):
            args.legend=[pre+lab for pre in args.legprefix for lab in args.legend]
    mpl=(not(args.np) and not(args.pqg)) or args.eps!='noeps'
    if mpl:  # import and initialize matplotlib
        import matplotlib
        matplotlib.use('Qt5Agg')
        matplotlib.rcParams['lines.linewidth'] = args.linewidth
        import matplotlib.font_manager as fnt
        import matplotlib.pyplot as plt
        if not(args.offset):
            import matplotlib.ticker as tk
            marques=tk.ScalarFormatter(useOffset=False)
        colo = (plt.rcParams['axes.prop_cycle'].by_key()['color'])*3
        if args.colors:  # if flag -co present, overwrite default colors
            colo[:len(args.colors)] = args.colors
        fig=plt.figure(1)
        mpl_keys = ('title','xlim','xlabel','xscale','ylim','ylabel','yscale')
        axes_kwargs = {k: args.__dict__[k] for k in mpl_keys 
                       if k in args.__dict__ and args.__dict__[k]}
        graf=fig.add_subplot(111,**axes_kwargs)
    if args.pqg: # import PyQtGraph if specified
        import pyqtgraph as pqg
        pqgPlot = pymp.pqgCustomPlot(title=args.title,
                              xlabel=args.xlabel,
                              ylabel=args.ylabel,
                              xrng=args.xlim,
                              yrng=args.ylim,
                              xlogscale=True if args.xscale=='log' else False,
                              ylogscale=True if args.yscale=='log' else False)
        pqgPlot.set_pqgWindow()

colcount=0  # overall plot counter, used for pqg color
legcount=0  # legend label counter
fpat=re.compile(r'(?P<nom>[^/\.]+)\.')  # regular expression to obtain the name of the file without extension
for filecount, doc in enumerate(args.files): #loop over each file
    if args.headers:  # print headers
        hdr, data=pym.read_mesafile(doc)
        print(doc)
        pym.terminal_print(data.columns, columns=args.terminalcols, order=args.order)
    else: 
        docols=[col for col in re.split(',', args.columns[filecount])]  # get headers to plot
        hdr, data=pym.read_mesafile(doc, usecols=docols)
        numplots=len(docols)-1
        if args.legend:  # check legend labels
            leg=args.legend[legcount:legcount+numplots]
            legcount+=numplots
        else:  # if unexistent, set legend labels to corresponent header
            leg=['']*numplots
            for numpl, pl in enumerate(docols[1:]):
                leg[numpl]=pl
        x=data[docols[0]].astype('float')  # set x values to first parsed column 
        for i in range(numplots):
            y=data[docols[i+1]].astype('float')
            if args.pqg:
                if args.colors:
                    pqgPlot.plot(x, y, color=args.colors[colcount], label=leg[i])
                else:
                    pqgPlot.plot(x, y, color=(colcount, max(allplots,9)), label=leg[i])
            if mpl:
                graf.plot(x, y, color=colo[colcount], label=leg[i])
            colcount+=1

if not(args.headers):
    if mpl:
        if not(args.offset):
            graf.yaxis.set_major_formatter(marques)  # set axis marker format
            graf.xaxis.set_major_formatter(marques) 
        graf.grid(True)
        graf.legend(loc='best', prop=fnt.FontProperties(size='medium'), title=args.legtit)
        fig.tight_layout()
    if args.eps!='noeps':  # save figure
        if args.eps!='sieps':  # save figure with specified name, extension is checked
            seed=fpat.search(args.eps) 
            if seed:
                figname=seed.group('nom')+'.eps' 
            else:
                figname=args.eps+'.eps' 
        else:  # set figure name to input file name
            seed=fpat.search(args.files[0])
            if seed:
                figname=seed.group('nom')+'.eps'
            else:
                figname=args.files[0]+'.eps'
        fig.savefig(figname, format='eps', dpi=1000)
    if not(args.np):
        if args.pqg:
            pqgPlot.show_pqgWindow()
        else:    
            plt.show()  # show figure with matplotlib
