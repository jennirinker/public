"""
A series of Python functions for working with the wind-related files for FAST
analyses.

Written by Jenni Rinker, Duke University.

Contact: jennifer.rinker@duke.edu

"""
import numpy as np
import os
from struct import unpack
from warnings import warn


def GetFirstWind(wind_fpath):
    """ First wind speed from file
    
        Args:
            wind_fpath (string): path to wind file
            
        Returns:
            u0 (float): initial wind value
    """
    
    # if it's a .wnd file
    if wind_fpath.endswith('.wnd'):
        
        # try to read it as a text file
        try:
            with open(wind_fpath,'r') as f:
                f.readline()
                f.readline()
                f.readline()
                first_line = f.readline().split()
                u0 = float(first_line[1])
                
        # if error, try to read as binary file
        except:
            turb  = readModel(wind_fpath)           # read file
            u0    = turb[0,:,:,0].mean()            # take mean of u(t0)
    
    # if it's a .bts file
    elif wind_fpath.endswith('.bts'):
        
        turb  = readModel(wind_fpath)            # read file
        u0    = turb[0,:,:,0].mean()            # take mean of u(t0)
        
    # if it's a .bl file
    elif wind_fpath.endswith('.bl'):
        
        turb  = readModel(wind_fpath)            # read file
        u0    = turb[0,:,:,0].mean()            # take mean of u(t0)

    else:
        errStr = 'Uncoded file extension ' + \
                        '\"{:s}\"'.format(wind_fpath.endswith())
        ValueError(errStr)
        
    return u0
        
# =============================================================================
# Code modified from PyTurbSim to load field from turbsim output
# Levi Kilcher, http://lkilcher.github.io/pyTurbSim/
    
# define endian-ness
e = '<'  

# ------------------------------ functions ------------------------------------
def readModel(fname, ):
    """
    Read a TurbSim data and input file and return a
    :class:`tsdata <pyts.main.tsdata>` data object.

    Parameters
    ----------
    fname : str
            The filename to load.
            If the file ends in:
              .bl or .wnd,  the file is assumed to be a bladed-format file.
              .bts, the file is assumed to be a TurbSim-format file.
    Returns
    -------
    turb : :class:`numpy.ndarray`
             [3 x n_z x n_y x n_t] array of wind velocity values
    """
    
    if (fname.endswith('wnd')):
        return bladed(fname,)
    elif (fname.endswith('bl')):
        return bladed(fname,)
    elif (fname.endswith('bts')):
        return turbsim(fname,)

    # Otherwise try reading it as a .wnd file.
    bladed(fname)  # This will raise an error if it doesn't work.    
    
    
def bladed(fname,):
    """
    Read Bladed format (.wnd, .bl) full-field time-series binary data files.

    Parameters
    ----------
    fname : str
            The filename from which to read the data.

    Returns
    -------
    turb : :class:`numpy.ndarray`
             [3 x n_z x n_y x n_t] array of wind velocity values

    """
    fname = checkname(fname, ['.wnd', '.bl'])
    with file(fname, 'rb') as fl:
        junk, nffc, ncomp, lat, z0, center = unpack(e + '2hl3f', fl.read(20))
        if junk != -99 or nffc != 4:
            raise IOError("The file %s does not appear to be a valid 'bladed (.bts)' format file."
                          % fname)
        ti = np.array(unpack(e + '3f', fl.read(12))) / 100
        dz, dy, dx, n_f, uhub = unpack(e + '3flf', fl.read(20))
        n_t = int(2 * n_f)
        fl.seek(12, 1)  # Unused bytes
        clockwise, randseed, n_z, n_y = unpack(e + '4l', fl.read(16))
        fl.seek(24, 1)  # Unused bytes
        nbt = ncomp * n_y * n_z * n_t
        turb = np.rollaxis(np.fromstring(fl.read(2 * nbt), dtype=np.int16)
                          .astype(np.float32).reshape([ncomp,
                                                       n_y,
                                                       n_z,
                                                       n_t], order='F'),
                          2, 1)
    turb[0] += 1000.0 / ti[0]
    turb /= 1000. / (uhub * ti[:, None, None, None])
    # Create the grid object:
    dt = dx / uhub
    # Determine the clockwise value.
    if clockwise == 0:
        try:
            d = sum_scan(convname(fname, '.sum'))
            clockwise = d['clockwise']
        except IOError:
            warn("Value of 'CLOCKWISE' not specified in binary file, "
                 "and no .sum file found. Assuming CLOCKWISE = True.")
            clockwise = True
        except KeyError:
            warn("Value of 'CLOCKWISE' not specified in binary file, "
                 "and %s has no line containing 'clockwise'. Assuming "
                 "CLOCKWISE = True." % convname(fname, '.sum'))
            clockwise = True
    else:
        clockwise = bool(clockwise - 1)
    if clockwise:
        # flip the data back
        turb = turb[:, :, ::-1, :]

    return turb, dt


def turbsim(fname):
    """
    Read TurbSim format (.bts) full-field time-series binary
    data files.

    Parameters
    ----------
    fname : str
            The filename from which to read the data.

    Returns
    -------
    turb : :class:`numpy.ndarray`
             [3 x n_z x n_y x n_t] array of wind velocity values

    """
    fname = checkname(fname, ['.bts'])
    u_scl = np.zeros(3, np.float32)
    u_off = np.zeros(3, np.float32)
    fl = file(fname, 'rb')
    (junk,
     n_z,
     n_y,
     n_tower,
     n_t,
     dz,
     dy,
     dt,
     uhub,
     zhub,
     z0,
     u_scl[0],
     u_off[0],
     u_scl[1],
     u_off[1],
     u_scl[2],
     u_off[2],
     strlen) = unpack(e + 'h4l12fl', fl.read(70))    
    desc_str = fl.read(strlen)  # skip these bytes.
    # load turbulent field
    nbt = 3 * n_y * n_z * n_t
    turb = np.rollaxis(np.fromstring(fl.read(2 * nbt), dtype=np.int16).astype(
        np.float32).reshape([3, n_y, n_z, n_t], order='F'), 2, 1)
    turb -= u_off[:, None, None, None]
    turb /= u_scl[:, None, None, None]
    return turb

def sum_scan(filename,):
    """
    Scan a sum file for specific variables.

    Parameters
    ----------
    filename : string
        The file to scan.

    Returns
    -------
    out : dict
        A dictionary of values identified.
    """
    # Currently this routine only searches for 'clockwise'.
    out = dict()
    with open(checkname(filename, ['.sum', '.SUM']), 'r') as infl:
        for ln in infl:
            ln = ln.lower()
            if 'clockwise' in ln.lower():
                v = ln.split()[0]
                if v in ['t', 'y']:
                    out['clockwise'] = True
                else:
                    out['clockwise'] = False
    return out
    

def convname(fname, extension=None):
    """
    Change the file extension.
    """
    if extension is None:
        return fname
    if extension != '' and not extension.startswith('.'):
        extension = '.' + extension
    return fname.rsplit('.', 1)[0] + extension

def checkname(fname, extensions=[]):
    """Test whether fname exists.

    If it does not, change the file extension in the list of
    extensions until a file is found. If no file is found this
    function raises IOError.
    """
    if os.path.isfile(fname):
        return fname
    if isinstance(extensions, basestring):
        # If extensions is a string make it a single-element list.
        extensions = [extensions]
    for e in extensions:
        fnm = convname(fname, e)
        if os.path.isfile(fnm):
            return fnm
    raise IOError("No such file or directory: '%s', and no "
                  "files found with specified extensions." % fname)
                  
