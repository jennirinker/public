"""
A series of Python functions for working with the wind-related files for FAST
analyses.

Written by Jenni Rinker, Duke University.

Contact: jennifer.rinker@duke.edu

TODO ********************
    - Rewrite GetFirstWind so it does not depend on PyTurbSim
"""
import pyts.io.main as io

def GetFirstWind(wind_fpath):
    """ First wind speed from file
    
        Args:
            wind_fpath (string): path to wind file
            
        Returns:
            u0 (float): initial wind value
    """

    # if it's a .wnd file (text)
    if wind_fpath.endswith('.wnd'):
        with open(wind_fpath,'r') as f:
            for i in range(3):
                f.readline()
            u0 = float(f.readline().split()[1])
    
    # if it's a .bts file
    elif wind_fpath.endswith('.bts'):
        
        tsout = io.readModel(wind_fpath)            # read file
        u0    = tsout.u[:,:,0].mean()               # average first wind

    else:
        errStr = 'Can only analyze .wnd (text) and .bts files'
        ValueError(errStr)

    return u0
    

def GetLastTime(wind_fpath):
    """ Last time step from wind file
    
        Args:
            wind_fpath (string): path to wind file
            
        Returns:
            tf (float): final time step
    """

    # if it's a .wnd file (text)
    if wind_fpath.endswith('.wnd'):
        with open(wind_fpath,'r') as f:
            f.seek(-1024, 2)
            last_line = f.readlines()[-1].decode()
            tf = float(last_line[0])
    
    # if it's a .bts file
    elif wind_fpath.endswith('.bts'):
        
        tsout = io.readModel(wind_fpath)            # read file
        tf    = tsout.t[-1]                         # last time value

    else:
        errStr = 'Can only analyze .wnd (text) and .bts files'
        ValueError(errStr)

    return tf