"""
A series of Python functions for the creation and analysis of FAST-related
files.

AUTHOR:  Jenni Rinker, Duke University
CONTACT: jennifer.rinker@duke.edu

===============================================================================

NOTES:
    Wind turbine template directory (FAST 7)
    ----------------------------------------
    Code is structured under the assumption that any wind turbine template 
    directories for FAST 7 have non-wind-dependent files (i.e., blade, tower,
    and control files) in the top level of the directory, wind-dependent 
    templates (i.e., AeroDyn and FAST templates) are in subfolder "templates", 
    and steady-state look-up table is in subfolder "steady_state" with the name 
    "<turb_name>_SS.mat".

===============================================================================
"""

# module dependencies
import jr_wind
import os, sys, json, re
import scipy.io as scio
import numpy as np


def WriteFAST7InputsAll(tmpl_dir,turb_name,wind_dir,
                      **kwargs):
    """ Write FAST 7 input files for all wind files in directory. Assumes wind 
        turbine template directory has organization specified in module 
        docstring. If output directory is specified, all FAST input files are 
        either written or copied to specified directory.
    
        Args:
            tmpl_dir (string): path to wind turbine template directory
            wind_fpaths (list): list of file paths to wind files
            wr_dir (string): directory to write input files to [opt]
            kwargs (dictionary): keyword arguments to WriteFAST7InputsOne [opt]
            
    """
    
    # possible wind file endings
    wind_ends = ('.bts','.wnd')
            
    # get list of wind files from directory
    wind_fnames = [f for f in os.listdir(wind_dir) if f.endswith(wind_ends)]

    # loop through wind files
    for wind_fname in wind_fnames:
        WriteFAST7InputsOne(tmpl_dir,turb_name,wind_fname,
                   wind_dir=wind_dir,
                   **kwargs)
    
    return
    
def WriteFAST7InputsOne(tmpl_dir,turb_name,wind_fname,
                   BlPitch0=None,RotSpeed0=None,
                   wind_dir=None,fileID=None,t_max=630.,
                   wr_dir=None):
    """ Write FAST 7 input files for one wind file. Assumes wind 
        turbine template directory has organization specified in module 
        docstring. If output directory is specified, all FAST input files are 
        either written or copied to specified directory.
    
        Args:
            tmpl_dir (string): path to turbine FAST directory
            turb_name (string): turbine name
            wind_fname (string): name of wind file
            wind_dir (string): path to directory with wind files
            BlPitch0 (list/numpy array): initial blade pitch angles [opt]
            RotSpee0 (float): initial rotor speed [opt]
            fileID (string): file identifier [opt]
            t_max (float): maximum simulation time [opt]
            
    """

    
    # get initial wind speed
    wind_fpath = os.path.join(wind_dir,wind_fname)
    u0 = jr_wind.GetFirstWind(wind_fpath)
    
    print('Writing FAST files for \"{:s}\" '.format(turb_name) + \
            'with wind file {:s}'.format(wind_fpath))
    
    # set optional values as necessary
    GenDOF = 'True'
    if wind_dir is None:
        wind_dir = os.path.join(tmpl_dir,'Wind')
    if wr_dir is None:
        wr_dir = tmpl_dir
    if fileID is None:
        fAD_name  = wind_fname[:-4] + '_AD.ipt'
        fFST_name = wind_fname[:-4] + '.fst'
    else:
        fAD_name  = turb_name+'_'+fileID+'_AD.ipt'
        fFST_name = turb_name+'_'+fileID+'.fst'
    if BlPitch0 is None:
        mdict = scio.loadmat(os.path.join(tmpl_dir,'steady_state',
                                        turb_name+'_SS.mat'),squeeze_me=True)
        LUT        = mdict['SS']
        saveFields = [str(s).strip() for s in mdict['Fields']]
        BlPitch0 = np.interp(u0,LUT[:,saveFields.index('WindVxi')],
                            LUT[:,saveFields.index('BldPitch1')])*np.ones(3)
    if RotSpeed0 is None:
        mdict = scio.loadmat(os.path.join(tmpl_dir,'steady_state',
                                        turb_name+'_SS.mat'),squeeze_me=True)
        LUT        = mdict['SS']
        saveFields = [str(s).strip() for s in mdict['Fields']]
        RotSpeed0 = np.interp(u0,LUT[:,saveFields.index('WindVxi')],
                            LUT[:,saveFields.index('RotSpeed')])
    if t_max is None:
        t_max = jr_wind.GetLastTime(wind_fpath)

    # create filenames
    fAD_temp  = os.path.join(tmpl_dir,'templates',turb_name+'_AD.ipt')
    fAD_out   = os.path.join(wr_dir,fAD_name)
    fFST_temp = os.path.join(tmpl_dir,'templates',turb_name+'.fst')
    fFST_out  = os.path.join(wr_dir,fFST_name)
    
    # write AeroDyn file
    with open(fAD_temp,'r') as f_temp:
        with open(fAD_out,'w') as f_write:
            i_line = 0
            for line in f_temp:
                if i_line == 9:
                    f_write.write(line.format(wind_fpath))
                else:
                    f_write.write(line)
                i_line += 1
                
    # write FAST file
    with open(fFST_temp,'r') as f_temp:
        with open(fFST_out,'w') as f_write:
            i_line = 0
            for line in f_temp:
                if i_line == 9:
                    f_write.write(line.format(t_max))
                elif i_line == 45:
                    f_write.write(line.format(BlPitch0[0]))
                elif i_line == 46:
                    f_write.write(line.format(BlPitch0[1]))
                elif i_line == 47:
                    f_write.write(line.format(BlPitch0[2]))
                elif i_line == 59:
                    f_write.write(line.format(GenDOF))
                elif i_line == 72:
                    f_write.write(line.format(RotSpeed0))
                elif i_line == 160:
                    f_write.write(line.format(fAD_name))
                else:
                    f_write.write(line)
                i_line += 1
                
    return
    
def CreateFAST7Dict(fast_fpath,
                    save=0,save_dir='.'):
    """ Build and save FAST 7 Python dictionary from input file
    
        Args:
            fast_fpath (string): path to .fst file
            
        Returns:
            TurbDict (dictionary): dictionary of turbine parameters
    """
    
    # ensure path is to a .fst file 
    if not fast_fpath.endswith('.fst'):
        err_str = 'Path {:s} is not to a FAST 7 input file'.format(fast_fpath)
        ValueError(err_str)
        
    # get turbine name and location, change to turbine directory
    turb_dir   = os.path.dirname(fast_fpath)
    fast_fname = os.path.basename(fast_fpath)
    
    print('\nCreating FAST 7 dictionary...')
    print('  FAST 7 file: {:s}'.format(fast_fname))
    print('  Directory:   {:s}\n'.format(turb_dir))
    
    # change to turbine directory, keep current directory
    old_dir = os.getcwd()
    os.chdir(turb_dir)
    
    # ====================== initialize dictionary ============================
    TurbDict = {}
    TurbDict['TurbName'] = fast_fname[:-4]
    TurbDict['TurbDir']  = turb_dir
    
    print('\n  Processing files...')
        
    # ==================== read data from .fst file ===========================
        
    sys.stdout.write('    FAST file:     {:s}...'.format(fast_fname))
    
    with open(fast_fname,'r') as f:
        
        # read first four lines manually
        f.readline()
        f.readline()
        TurbDict['FASTCmnt1'] = f.readline().rstrip('\n')
        TurbDict['FASTCmnt2'] = f.readline().rstrip('\n')
        
        # read through BldGagNd automatically
        key = ''
        while ( key != 'BldGagNd'):
            line = f.readline()
            
            # if line doesn't start with dashes, it is a parameter
            if ( line[:2] != '--' ):
                # convert to float if number
                try:
                    value = float(line.split()[0])
                # otherwise it's a string; remove quotes if present
                except ValueError:
                    value = line.split()[0].rstrip('\"').lstrip('\"')
                key   = line.split()[1]
                TurbDict[key] = value

        # read OutList automatically but save differently than above
        OutList = []
        line = f.readline()             # skip line with "OutList"
        line = f.readline()
        end  = 0
        while not end:
            if (line[:3] == 'END'):
                end = 1
            else:
                OutList.append(line)
                line = f.readline()
        TurbDict['OutList'] = OutList
        
    sys.stdout.write('processed.\n')
            
    # ============== read data from platform file if used =====================
    if TurbDict['PtfmModel']:
        
        sys.stdout.write('    Platform file:' + \
                                ' {:s}...'.format(TurbDict['PtfmFile']))
    
        with open(TurbDict['PtfmFile'],'r') as f:
            
            # read first four lines manually
            f.readline()
            f.readline()
            line = f.readline().rstrip('\n')
            TurbDict['PtfmCmnt'] = line
            
            # read remaining lines automatically
            line = f.readline().rstrip('\n')
            while ( line ):
                
                # if line doesn't start with dashes, it's a parameter
                if ( line[:2] != '--' ):
                    # convert to float if number
                    try:
                        value = float(line.split()[0])
                    # remove quotes if present
                    except ValueError:
                        value = line.split()[0].rstrip('\"').lstrip('\"')
                    key   = line.split()[1]
                    TurbDict[key] = value
                
                line = f.readline().rstrip('\n')
                
        sys.stdout.write('processed.\n')
            
    # =================== read data from tower file ===========================
         
    sys.stdout.write('    Tower ' + \
                        'file:    {:s}...'.format(TurbDict['TwrFile']))
             
    with open(TurbDict['TwrFile'],'r') as f:
        
        # read first four lines manually
        f.readline()
        f.readline()
        line = f.readline().rstrip('\n')
        TurbDict['TwrCmnt'] = line
        
        # read to HtFract automatically
        value = ''
        while ( value != 'HtFract'):
            line = f.readline()
            
            # if line doesn't start with dashes, it is a parameter
            if ( line[:2] != '--' ):
                # convert to float if number
                try:
                    value = float(line.split()[0])
                # otherwise remove quotes if present
                except ValueError:
                    value = line.split()[0].rstrip('\"').lstrip('\"')
                key   = line.split()[1]
                TurbDict[key] = value
        f.readline()
        
        # read distributed tower properties
        twr_prop = []
        for i_st in range(int(TurbDict['NTwInpSt'])):
            line = f.readline()
            twr_prop.append([float(s) for s in line.rstrip('\n').split()])
        TurbDict['TwrSched'] = twr_prop
        
        # read remaining lines automatically
        line = f.readline().rstrip('\n')
        while ( line ):
            
            # if line doesn't start with dashes, it's a parameter
            if ( line[:2] != '--' ):
                # convert to float if number
                try:
                    value = float(line.split()[0])
                # remove quotes if present
                except ValueError:
                    value = line.split()[0].rstrip('\"').lstrip('\"')
                key   = line.split()[1]
                TurbDict[key] = value
            
            line = f.readline().rstrip('\n')  
            
    sys.stdout.write('processed.\n')
                    
    # =============== read data from furling file if used =====================
    if ( TurbDict['Furling'] == 'True' ):
        
        sys.stdout.write('    Furling ' + \
                        'file:  {:s}...'.format(TurbDict['FurlFile']))
             
        with open(TurbDict['FurlFile'],'r') as f:
            
            # read first four lines manually
            f.readline()
            f.readline()
            line = f.readline().rstrip('\n')
            TurbDict['FurlCmnt'] = line
            
            # read remaining lines automatically
            line = f.readline().rstrip('\n')
            while ( line ):
                
                # if line doesn't start with dashes, it's a parameter
                if ( line[:2] != '--' ):
                    # convert to float if number
                    try:
                        value = float(line.split()[0])
                    # remove quotes if present
                    except ValueError:
                        value = line.split()[0].rstrip('\"').lstrip('\"')
                    key   = line.split()[1]
                    TurbDict[key] = value
                
                line = f.readline().rstrip('\n')
                
        sys.stdout.write('processed.\n')
            
    # =================== read data from blade files ==========================
                
    for i_bl in range(1,int(TurbDict['NumBl'])+1):
        
        # blade-specific keys
        bl_str = '_' + str(i_bl)                    # append '_x' to keys
        bl_key = 'BldFile({:d})'.format(i_bl)       # blade file key
        
        sys.stdout.write('    Blade {:d} '.format(i_bl) + \
                        'file:  {:s}...'.format(TurbDict[bl_key]))
                     
        with open(TurbDict[bl_key],'r') as f:
            
            # read first four lines manually
            f.readline()
            f.readline()
            line = f.readline().rstrip('\n')
            TurbDict['BldCmnt' + bl_str] = line
            
            # read to BlFract automatically
            value = ''
            while ( value != 'BlFract'):
                line = f.readline()
                
                # if line doesn't start with dashes, it is a parameter
                if ( line[:2] != '--' ):
                    # convert to float if number
                    try:
                        value = float(line.split()[0])
                    # otherwise remove quotes if present
                    except ValueError:
                        value = line.split()[0].rstrip('\"').lstrip('\"')
                    key   = line.split()[1] + bl_str
                    TurbDict[key] = value
            f.readline()
            
            # read distributed blade properties
            BldSched = []
            for i_st in range(int(TurbDict['NBlInpSt' + bl_str])):
                line = f.readline()
                BldSched.append([float(s) for s in line.rstrip('\n').split()])
            TurbDict['BldSched' + bl_str] = BldSched
            
            # read remaining lines automatically
            line = f.readline().rstrip('\n')
            while ( line ):
                
                # if line doesn't start with dashes, it's a parameter
                if ( line[:2] != '--' ):
                    # convert to float if number
                    try:
                        value = float(line.split()[0])
                    # remove quotes if present
                    except ValueError:
                        value = line.split()[0].rstrip('\"').lstrip('\"')
                    key   = line.split()[1] + bl_str
                    TurbDict[key] = value
                
                line = f.readline().rstrip('\n') 
               
        sys.stdout.write('processed.\n')
             
    # =================== read data from AeroDyn file =========================
        
    sys.stdout.write('    AeroDyn ' + \
                        'file:  {:s}...'.format(TurbDict['ADFile']))
             
    with open(TurbDict['ADFile'],'r') as f:
        
        # read first line manually
        line = f.readline().rstrip('\n')
        TurbDict['ADCmnt'] = line
        
        # read to NumFoil automatically
        key = ''
        while ( key != 'NumFoil'):
            line = f.readline()
            
            # if line doesn't start with dashes, it is a parameter
            if ( line[:2] != '--' ):
                # convert to float if number
                try:
                    value = float(line.split()[0])
                # otherwise remove quotes if present
                except ValueError:
                    value = line.split()[0].rstrip('\"').lstrip('\"')
                key   = line.split()[1]
                TurbDict[key] = value
        
        # read foil files
        foil_prop = []
        for i_st in range(int(TurbDict['NumFoil'])):
            line = f.readline().split()[0].lstrip('\"').rstrip('\"\n')
            foil_prop.append(line)
        TurbDict['FoilNm'] = foil_prop
        
        # read number of blade nodes
        line = f.readline()     
        # convert to float if number
        try:
            value = float(line.split()[0])
        # otherwise remove quotes if present
        except ValueError:
            value = line.split()[0].rstrip('\"').lstrip('\"') 
        key   = line.split()[1]
        TurbDict[key] = value
        f.readline()
        
        # read blade nodes
        AD_prop = []
        for i_bl in range(int(TurbDict['BldNodes'])):
            line = f.readline().rstrip('\n').split()
            row = []
            for i_col in range(len(line)):
                try:
                    row.append(float(line[i_col]))
                except ValueError:
                    row.append(line[i_col])
            AD_prop.append(row)
        TurbDict['ADSched'] = AD_prop
        
    sys.stdout.write('processed.\n')
                    
    # =============== read data from pitch file if used =====================
    if ( TurbDict['PCMode'] == 1):
        
        TurbDict['PitchFile'] = 'pitch.ipt'
        
        sys.stdout.write('    Pitch ' + \
                        'file:    pitch.ipt...')
             
        with open('pitch.ipt','r') as f:
            
            # read first line manually
            line = f.readline().rstrip('\n')
            TurbDict['PitchCmnt'] = line
            
            # read through CNSTN(11) automatically
            key = ''
            while ( key != 'CNST(11)'):
                line = f.readline()
                value = float(line.split()[0])
                key   = line.split()[1]
                TurbDict[key] = value
            f.readline()                # skip empty line
            
            # read transfer functions manually
            TFNames = ['RPM2PI','RPM2P','TA2P','P2P']
            for i_tf in range(len(TFNames)):
                TF = TFNames[i_tf]
                Order = int(f.readline().split()[0])
                NumCoeffs = [float(x) for x in f.readline().split('Numerator')[0].split()]
                DenCoeffs = [float(x) for x in f.readline().split('Denominator')[0].split()]
                TurbDict[TF+'_Order'] = Order
                TurbDict[TF+'_Num']  = NumCoeffs
                TurbDict[TF+'_Den']  = DenCoeffs
                f.readline()                # skip empty line
                                    
        sys.stdout.write('processed.\n')
            
# TODO: load data from noise file, linearization file, ADAMS file
                
    # change back to original working directory
    os.chdir(old_dir)
    
    # save dictionary if requested
    if save:
        fpath_save = os.path.join(save_dir,TurbDict['TurbName']+'_Dict.dat')
        with open(fpath_save,'w') as fsave:
            json.dump(TurbDict,fsave)
        print('\nTurbDict saved to {:s}'.format(fpath_save))    
    
    return TurbDict
    
def WriteFAST7Template(dir_out,TurbDict):
    """ Create turbine-specific FAST v7.02 template file.
        Template can then be used to write wind-file-specic .fst files.
    
        Args:
            dir_out (string): directory to write template files to
            TurbDict (dictionary): dictionary of turbine parameters
            Comment (list): two-string list of header lines in FAST file 
        
    """

    turb_name     = TurbDict['TurbName']
    sys.stdout.write('\nWriting FAST 7 template for turbine {:s}...'.format(turb_name))
                        
    # define path to base template and output filename
    fpath_temp = os.path.join('templates','Template.fst')
    fpath_out  = os.path.join(dir_out,turb_name+'_template.fst')
    
    # get list of keys to skip (they depend on wind file)
    windfile_keys = ['TMax',
                 'BlPitch(1)','BlPitch(2)','BlPitch(3)',
                 'OoPDefl','IPDefl','TeetDefl','Azimuth',
                 'RotSpeed','NacYaw','TTDspFA','TTDspSS']
                    
    # open base template file and file to write to (turbine-specific template)
    with open(fpath_temp,'r') as f_temp:
        with open(fpath_out,'w') as f_write:
            
            # read each line in template file
            for r_line in f_temp:
                
                # default to copying without modification
                w_line = r_line
                                                        
                # if line has a write-able field
                if ('{:' in r_line):
                    
                    # get fieldname, format for value, and remaining string
                    field = r_line.split()[1]
                    value_format = r_line.split(field)[0]
                    comment      = r_line.split(field)[-1]
                    
                    # check if comment line
                    if ('FASTCmnt' in field):
                        w_line = TurbDict[field] + '\n'
                        
                    # check if OutList
                    elif (field == 'OutList'):
                        for i_line in range(len(TurbDict['OutList'])-1):
                            f_write.write(TurbDict['OutList'][i_line])
                            w_line = TurbDict['OutList'][-1]
                    
                    # otherwise, if key is not to be skipped
                    elif (field not in windfile_keys):
# TODO: add try/except to load default value if field not in dictionary
                        value  = TurbDict[field]
                        w_line = field.join([value_format.format(value),
                                            comment])
                    
                f_write.write(w_line)
               
    print('done.')
    
    return


def WriteAeroDynTemplate(dir_out,TurbDict):
    """ AeroDyn input file for FAST v7.02
    """
        
    TurbName     = TurbDict['TurbName']
    sys.stdout.write('\nWriting AeroDyn v13 template for turbine {:s}...'.format(TurbName))
                        
    # define path to base template and output filename
    fpath_temp = os.path.join('templates','Template_AD.ipt')
    fpath_out  = os.path.join(dir_out,TurbName+'_AD_template.ipt')
    
    # open template file and file to write to
    with open(fpath_temp,'r') as f_temp:
        with open(fpath_out,'w') as f_write:
            
            # read each line in template file
            for r_line in f_temp:
                
                # default to copying without modification
                w_line = r_line
                                                        
                # if line has a write-able field
                if ('{:' in r_line):
                    
                    # get fieldname, format for value, and remaining string
                    field = r_line.split()[1]
                    value_format = r_line.split(field)[0]
                    comment      = r_line.split(field)[-1]
                    
                    # check if comment line
                    if ('ADCmnt' in field):
                        w_line = TurbDict[field] + '\n'
                        
                    # if foilnames, print them all
                    elif (field == 'FoilNm'):
                        FoilNames = TurbDict[field]
                        
                        # print first foilname manually
                        w_line    = field.join([value_format.format(FoilNames[0]),
                                            comment])
                        f_write.write(w_line)        
                        
                        # loop through remaining airfoils
                        for i_line in range(1,len(TurbDict['FoilNm'])):
                            f_write.write(FoilNames[i_line] + '\n')
                        w_line = ''
                        
                    # if foilnames, print them all
                    elif (field == 'ADSched'):      
                        
                        # loop through remaining airfoils
                        for i_line in range(0,len(TurbDict['ADSched'])):
                            w_line = value_format.format( \
                                        *TurbDict['ADSched'][i_line])
                            f_write.write(w_line + '\n')
                        w_line = ''
                    
                    # otherwise, print key normally
                    else:
# TODO: add try/except to load default value if field not in dictionary
                        value  = TurbDict[field]
                        w_line = field.join([value_format.format(value),
                                            comment])
                    
                f_write.write(w_line)
                
    print('done.')
    
    return


def WriteBladeFiles(dir_out,TurbDict):
    """ Blade input files for FAST v7.02
    """
        
    TurbName     = TurbDict['TurbName']
    print('\nWriting FAST v7.02 blade files for turbine {:s}...'.format(TurbName))
                        
    # define path to base template
    fpath_temp = os.path.join('templates','Template_Blade.dat')
    
    # loop through blades
    for i_bl in range(1,int(TurbDict['NumBl'])+1):
        
        sys.stdout.write('  Blade {:d}...'.format(i_bl))
    
        # get output paths and string appender for blade
        fname_out = TurbDict['BldFile({:d})'.format(i_bl)]
        fpath_out = os.path.join(dir_out,fname_out)
        bld_str   = '_{:d}'.format(i_bl)
    
        # open template file and file to write to
        with open(fpath_temp,'r') as f_temp:
            with open(fpath_out,'w') as f_write:
                
                # read each line in template file
                for r_line in f_temp:
                    
                    # default to copying without modification
                    w_line = r_line
                                                            
                    # if line has a write-able field
                    if ('{:' in r_line):
                        
                        # get fieldname, format for value, and remaining string
                        field = r_line.split()[1]
                        value_format = r_line.split(field)[0]
                        comment      = r_line.split(field)[-1]
                        
                        # check if comment line
                        if ('BldCmnt' in field):
                            w_line = TurbDict[field + bld_str] + '\n'
                                                    
                        # if blade schedule
                        elif (field == 'BldSched'):
                            
                            BldSched = TurbDict['BldSched' + bld_str]
                            
                            # loop blade schedule
                            for i_line in range(len(BldSched)):
                                w_line = value_format.format( \
                                            *BldSched[i_line])
                                f_write.write(w_line + '\n')
                            w_line = ''
                        
                        # otherwise, print key normally
                        else:
    # TODO: add try/except to load default value if field not in dictionary
                            value  = TurbDict[field + bld_str]
                            w_line = field.join([value_format.format(value),
                                                comment])
                        
                    f_write.write(w_line)
                    
            sys.stdout.write('done.\n')
    
    return


def WriteTowerFile(dir_out,TurbDict):
    """ Tower input files for FAST v7.02
    """
        
    TurbName     = TurbDict['TurbName']
    sys.stdout.write('\nWriting FAST v7.02 tower file for turbine {:s}...'.format(TurbName))
                        
    # define path to base template and output file
    fpath_temp = os.path.join('templates','Template_Tower.dat')
    fname_out = TurbDict['TwrFile']
    fpath_out = os.path.join(dir_out,fname_out)
    
    # open template file and file to write to
    with open(fpath_temp,'r') as f_temp:
        with open(fpath_out,'w') as f_write:
            
            # read each line in template file
            for r_line in f_temp:
                
                # default to copying without modification
                w_line = r_line
                                                        
                # if line has a write-able field
                if ('{:' in r_line):
                    
                    # get fieldname, format for value, and remaining string
                    field = r_line.split()[1]
                    value_format = r_line.split(field)[0]
                    comment      = r_line.split(field)[-1]
                    
                    # check if comment line
                    if ('TwrCmnt' in field):
                        w_line = TurbDict[field] + '\n'
                                                
                    # if blade schedule
                    elif (field == 'TwrSched'):
                        
                        TwrSched = TurbDict['TwrSched']
                        
                        # loop blade schedule
                        for i_line in range(len(TwrSched)):
                            w_line = value_format.format( \
                                        *TwrSched[i_line])
                            f_write.write(w_line + '\n')
                        w_line = ''
                    
                    # otherwise, print key normally
                    else:
# TODO: add try/except to load default value if field not in dictionary
                        value  = TurbDict[field]
                        w_line = field.join([value_format.format(value),
                                            comment])
                    
                f_write.write(w_line)
                
        sys.stdout.write('done.\n')

    return


def WritePitchCntrl(dir_out,TurbDict):
    """ Pitch control routine for Kirk Pierce controller for FAST v7.02
    """
        
    TurbName     = TurbDict['TurbName']
    sys.stdout.write('\nWriting FAST v7.02 pitch.ipt file for turbine {:s}...'.format(TurbName))
                        
    # define path to base template and output file
    fpath_temp = os.path.join('templates','Template_pitch.ipt')
    fname_out = TurbDict['PitchFile']
    fpath_out = os.path.join(dir_out,fname_out)
    
    # open template file and file to write to
    with open(fpath_temp,'r') as f_temp:
        with open(fpath_out,'w') as f_write:
            
            # read each line in template file
            for r_line in f_temp:
                
                # default to copying without modification
                w_line = r_line
                                                        
                # if line has a write-able field
                if ('{:' in r_line):
                    
                    # get fieldname, format for value, and remaining string
                    # check if "Num" or "Den" in field
                    field = r_line.split()[1]
                    value_format = r_line.split(field)[0]
                    comment      = r_line.split(field)[-1]
                    num_or_den   = [s for s in ('Num','Den') if s in field]
                    
                    # check if comment line
                    if ('PitchCmnt' in field):
                        w_line = TurbDict[field] + '\n'
                        
                    # check if it's a transfer function order
                    elif ('Order' in field):
                        w_line = '{:4d}      {:s}'.format(TurbDict[field], \
                                                            comment)
                                                            
                    # else if numerator or denominator, loop through transfer fcn
                    elif num_or_den:
                        TF = field.split('_')[0]
                        TF_Coeffs = TurbDict[TF+'_'+num_or_den[0]]
                        for i_order in range(len(TF_Coeffs)):
                            f_write.write(value_format.format( \
                                                    TF_Coeffs[i_order]))
                        w_line = comment
                        
                    # otherwise, print key normally
                    else:
# TODO: add try/except to load default value if field not in dictionary
                        value  = TurbDict[field]
                        w_line = field.join([value_format.format(value),
                                            comment])
                    
                f_write.write(w_line)
                
        sys.stdout.write('done.\n')

    return
