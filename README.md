# MESA utilities
Python scripts to analyze data from Modules for Experiments in Stellar Astrophysics using existing libraries to import data. In particular, the main difference with existing MESA-specific libraries, `pandas` module is used, allowing fast file reading.

These codes are developed as a tool for my end of degree thesis. There are 2 kinds of files: scripts wich make use of argparse in order to be executed directly from the command line and files containing collections of functions, which are inside the . 

In order to be able to import the functions, the path of the repository has to be added with the `sys` module. Below there is an example of how to import the functions without the need of any `setup.py`:

    import sys
    sys.path.append('/path/to/pyMESA/')
    import pymesa.tools as pym

There is also the option of using `PYTHONPATH` instead, see this [link](http://www.mantidproject.org/Using_Modules) for more info.

Many of the codes use already existing libraries to import and plot data 
from MESA results:
- [mesaPlot](https://github.com/rjfarmer/mesaplot)
- [NuGridPy](https://github.com/NuGrid/NuGridPy)

Therefore, they may require to have at least one of them installed. If both mesaPlot and nugridpy are correctly installed, all the codes should work properly.
