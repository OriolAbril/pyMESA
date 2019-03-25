from pyqtgraph.Qt import QtGui
import pyqtgraph as pqg


class CustomPlot:
    r"""
    Class containing the most usual plot variables'

    Parameters:
    -----------

    gtitle : str
        Ritle of the plot

    xlabel,ylabel : str
        Labels of the axis

    xrng,yrng : array-like (lenght=2), None
        Limits of the axis, rng[0] will be on the left/lower
        part of the plot, even if it means inverting the axis

    xlogscale,ylogscale : boolean, default False
    """

    def __init__(
        self,
        title="",
        xlabel="",
        ylabel="",
        xrng=None,
        yrng=None,
        xlogscale=False,
        ylogscale=False,
    ):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.xlim = xrng
        self.ylim = yrng
        self.xlog = xlogscale
        self.ylog = ylogscale


class pqgCustomPlot(CustomPlot):
    r"""
    Class wrapping basic plotting functions with pyqtgraph
    """

    def __init__(
        self,
        wtitle="pyMESA",
        title="",
        xlabel="",
        ylabel="",
        xrng=None,
        yrng=None,
        xlogscale=False,
        ylogscale=False,
    ):
        CustomPlot.__init__(
            self, title, xlabel, ylabel, xrng, yrng, xlogscale, ylogscale
        )
        self.wtitle = wtitle

    def set_pqgWindow(self):
        r"""
        Function to initialize a pyqtgraph plot.

        Parameters:
        -----------

        wtitle : str
            Title of the Qt window

        Generates:
        --------

        app : PyQt.QtWidgets.QApplication
            Initialized Qt application

        mw : PyQt5.QtWidgets.QMainWindow
            Main window of the QtGui

        cw : PyQt5.QtWidgets.QWidget
            Central widget of the main window

        layout : PyQt5.QtWidgets.QVBoxLayout

        pw : pyqtgraph.widgets.PlotWidget.PlotWidget
            PlotWidget in the central widget
        """
        ## Switch to using white background and black foreground
        pqg.setConfigOption("background", "w")
        pqg.setConfigOption("foreground", "k")
        self.app = QtGui.QApplication([])  # initialize Qt
        self.mw = QtGui.QMainWindow()  # initialize main window
        self.mw.setWindowTitle(self.wtitle)  # set window title
        # initialize widget and layout
        self.cw = QtGui.QWidget()
        self.mw.setCentralWidget(self.cw)
        self.layout = QtGui.QVBoxLayout()
        self.cw.setLayout(self.layout)
        # create plot and add it to main widget
        self.pw = pqg.PlotWidget(enableMenu=True)
        self.layout.addWidget(self.pw)
        self.pw.setLabels(left=self.ylabel, bottom=self.xlabel, title=self.title)
        if self.xlim or self.ylim:
            self.pw.setRange(xRange=self.xlim, yRange=self.ylim)
        if self.xlim:
            self.pw.invertX(False if (self.xlim[1] - self.xlim[0]) > 0 else True)
        if self.ylim:
            self.pw.invertY(False if (self.ylim[1] - self.ylim[0]) > 0 else True)
        self.pw.setLogMode(x=self.xlog, y=self.ylog)
        self.pw.addLegend()  # legend must be set here in order to be "filled"
        self.pw.showGrid(x=True, y=True, alpha=0.5)

    def plot(self, x, y, label=None, color=0):
        self.pw.plot(x, y, name=label, pen=color)

    def show_pqgWindow(self):
        r"""
        Show plot window.
        """
        ## Display the widget as a new window
        self.pw.update()
        self.mw.show()
        ## Start the Qt event loop
        self.app.exec_()
