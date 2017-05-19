# import libraries
import argparse as arp  # command line parsing module and help
import numpy as np 
import re  # regular expressions
import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym

p=arp.ArgumentParser(prog='MESA_grafics', description='Script to plot data from the .data output files from MESA')
p.add_argument('--version', action='version', version='%(prog)s 0.2')
p.add_argument('files', metavar='FILES', help='Name of the .data type file/s with the extension', nargs='+')
group=p.add_mutually_exclusive_group(required=True)
group.add_argument('-hd', '--headers', help='Show available headers in the files. Default: False', 
                   action='store_true', default=False)
group.add_argument('-c', '--columns', help='Columns to be plotted, the first one will be used as x values.\
                   The separation between columnes for the same file should be a comma and between different\
                   files a space.', nargs='+')
p.add_argument('-s', '--separator', help='Separator character/s or regular expression to match the separator',
               type=str, default=r'\s+')
pltpar=p.add_argument_group(title='Commands to personalize plots')
pltpar.add_argument('-pqg', help='Use PyQtGraph as plotting module instead of Matplotlib', action='store_true',
                    default=False)
pltpar.add_argument('-np', help='Do not show the plot. Default: False', action='store_true', default=False)
pltpar.add_argument('-off', '--offset', help='Use matplotlib''s default offest in axis ticks. Default:False', 
                    action='store_true', default=False)
pltpar.add_argument('-eps', help='Write matplotlib plot as an Encapsulated PostScript. The name can be specified',
                    type=str, nargs='?', default='noeps', const='sieps')
pltpar.add_argument('-sc', '--scale', help='Choose the scale between: liner, semilogy, semilogx or logxy',
                    type=str, choices=['lin', 'logy', 'logx', 'loglog', 'logxy'])
pltpar.add_argument('-co', '--colors', help='Colors to be used in the plot, they must be valid matplotlib colors',
                    nargs='+')
pltpar.add_argument('-l', '--legend', help='Labels for the legend. Default text is name of file without extension',
                    nargs='+')
pltpar.add_argument('-t', '--title', help='Title of the plot', type=str, default='')
pltpar.add_argument('-lt', '--legtit', help='Title for the legend', type=str, default='')
pltpar.add_argument('-xl', '--xlabel', help='Label of the x axis', type=str)
pltpar.add_argument('-yl', '--ylabel', help='Label of the y axis', type=str, default='')
pltpar.add_argument('-x', '--xaxis', help='Set the xaxis limits', nargs=2, type=float)
pltpar.add_argument('-y', '--yaxis', help='Set the yaxis limits', nargs=2, type=float)
args=p.parse_args()  # parse arguments

if not(args.headers):  # set plot variables and configuration
    if len(args.files)!=len(args.columns):
        args.columns=[args.columns[0]]*len(args.files)
    allplots=0
    comapat=re.compile(',')
    for comas in [comapat.findall(i) for i in args.columns]:
        allplots+=len(comas)
    if args.scale=='loglog':
        args.scale='logxy'
    if not(args.xlabel):
        args.xlabel=args.columns[0].split(',')[0]
    colo=['blue', 'black', 'red', 'green', 'yellow', 'cyan', 'magenta']*3  # set default colors
    if args.colors:  # if flag -co present, overwrite default colors
        for colnum,col in enumerate(args.colors):
            colo[colnum]=col
    mpl=(not(args.np) and not(args.pqg))
    if (mpl or args.eps!='noeps'):  # import and initialize matplotlib
        import matplotlib
        matplotlib.use('TKAgg')
        import matplotlib.font_manager as fnt
        import matplotlib.pyplot as plt
        if not(args.offset):
            import matplotlib.ticker as tk
            marques=tk.ScalarFormatter(useOffset=False)
        fig=plt.figure(1)
        graf=fig.add_axes([0.13, 0.1, 0.8, 0.8])
    if args.pqg: # import PyQtGraph if specified
        import PyQt5
        from pyqtgraph.Qt import QtGui, QtCore
        import pyqtgraph as pqg
        ## Switch to using white background and black foreground
        pqg.setConfigOption('background', 'w')
        pqg.setConfigOption('foreground', 'k')
        app = QtGui.QApplication([])  # initialize Qt
        mw = QtGui.QMainWindow()  # initialize main window
        mw.setWindowTitle('pyMESA') #set window title
        # initialize widget and layout
        cw = QtGui.QWidget()
        mw.setCentralWidget(cw)
        l = QtGui.QVBoxLayout()
        cw.setLayout(l)
        # create plot and add it to main widget
        pw = pqg.PlotWidget(enableMenu=True)
        l.addWidget(pw)
        pw.setLabel('left', args.ylabel)
        pw.setLabel('bottom', args.xlabel)
        if args.xaxis:
            pw.setRange(xRange=args.xaxis)
            if args.xaxis[0]>args.xaxis[1]:
                pw.invertX(True)
        if args.yaxis:
            pw.setRange(yRange=args.yaxis)
            if args.yaxis[0]>args.yaxis[1]:
                pw.invertY(True)
        pw.setTitle(args.title)
        pw.addLegend()  # legend must be set here in order to be "filled"
        pw.showGrid(x=True, y=True, alpha=0.5)

# it is placed here in order to happen after importing matplotlib
import mesa as ms  

colcount=0  # overall plot counter, used for color
legcount=0  # legend label counter
fpat=re.compile(r'(?P<nom>[^/\.]+)\.')  # regular expression to obtain the name of the file without extension
for filecount, doc in enumerate(args.files): #loop over each file
    length=pym.file_len(doc)
    hdr, cols, data=ms._read_mesafile(doc, length-6)
    if args.headers:  # print headers
        print doc
        pym.terminal_print(cols.keys())
        print '\n'
    else: 
        docols=[col for col in re.split(',',args.columns[filecount])]  # get headers to plot
        numplots=len(docols)-1
        if args.legend:  # check legend labels
            leg=args.legend[legcount:legcount+numplots]
            legcount+=numplots
        else:  # if unexistent, set legend labels to corresponent header
            leg=['']*numplots
            for numpl, pl in enumerate(docols[1:]):
                leg[numpl]=pl
        x=data[:, cols[docols[0]]-1].astype('float')  # set x values to first parsed column 
        for i in range(numplots):
            y=data[:, cols[docols[i+1]]-1].astype('float')
            if args.pqg:
                if args.colors:
                    pw.plot(x, y, pen=pqg.mkPen(args.colors[colcount]), name=leg[i])
                else:
                    pw.plot(x, y, pen=(colcount, allplots), name=leg[i])
            if (mpl or args.eps!='noeps'):
                graf.plot(x, y, color=colo[colcount], label=leg[i])
            colcount+=1
if not(args.headers):
    if (mpl or args.eps!='noeps'):
        # set axis labels and limits
        if args.xlabel:
            graf.set_xlabel(args.xlabel)
        graf.set_ylabel(args.ylabel)
        if args.yaxis: 
            graf.set_ylim(args.yaxis)
        if args.xaxis:
            graf.set_xlim(args.xaxis)
        if not(args.offset):
            graf.yaxis.set_major_formatter(marques)  # set axis marker format
            graf.xaxis.set_major_formatter(marques) 
        # set axis scale
        if (args.scale=='logx' or args.scale=='logxy'):
            graf.set_xscale('log')
        if (args.scale=='logy' or args.scale=='logxy'):
            graf.set_yscale('log')
        # set title, grid and legend
        fig.suptitle(args.title)
        graf.grid(True)
        graf.legend(loc='best', prop=fnt.FontProperties(size='medium'), title=args.legtit)
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
            ## Display the widget as a new window
            pw.update()
            mw.show()
            ## Start the Qt event loop
            app.exec_()
        else:    
            plt.show()  # show figure with matplotlib
