"""
A series of Python functions for the creation and analysis of FAST-related
files.

AUTHOR:  Jenni Rinker, Duke University
CONTACT: jennifer.rinker@duke.edu


NOTES:
    Currently only tested for FAST v7

TODO:
    - Proper handling of tower gage/blade gage nodes (currently only tested with none)
    - Porper handling of DISCON controller (currently breaks)

"""

# module dependencies
import jr_wind
import os, sys, json
import scipy.io as scio
import numpy as np


def WriteFastADAll(TurbName,ModlDir,WindDir,FastDir,
                   version=7,Naming=1,
                   **kwargs):
    """ Write FAST and AeroDyn input files for all wind files in directory
    
        Args:
            TurbName (string): turbine name
            ModlDir (string): directory with wind-independent files (e.g.,
                              Blade, Tower, Pitch files)
            WindDir (string): directory with wind files
            FastDir (string): directory to write FAST & AeroDyn files to
                                
        Keyword Args:
            version (int): FAST version (7 or 8)
            Naming (string): flag for naming convention for FAST files [opt]
                                1 = '<WindName>.fst'
                                2 = '<TurbName>_<WindName>.fst'
            kwargs (dictionary): keyword arguments to WriteFastADOne [opt]
    """
    
    # possible wind file endings
    wind_ends = ('.bts','.wnd','.bl')
            
    # get list of wind files from directory
    WindNames = [f for f in os.listdir(WindDir) if f.endswith(wind_ends)]

    # loop through wind files
    for WindName in WindNames:
        WindPath = os.path.join(WindDir,WindName)
        
        # set filename according to naming conventions
        if Naming == 1:
            FastName = os.path.splitext(WindName)[0]
        elif Naming == 2:
            FastName = TurbName + '_' + os.path.splitext(WindName)[0]
            
        # write FAST/AD files for 
        WriteFastADOne(TurbName,WindPath,FastName,
                       ModlDir,FastDir,version=version,
                       **kwargs)
    
    return
    
def WriteFastADOne(TurbName,WindPath,FastName,
                   ModlDir,FastDir,version=7,verbose=0,
                   **kwargs):
    """ Write FAST and AeroDyn input files for specified wind file
    
        Possible keyword arguments inclue any FAST initial conditions plus
        TMax and TStart.
    
        Args:
            TurbName (string): turbine name
            WindPath (string): path to wind file
            FastName (sring): name for .fst file (AD will be "<Name>_AD.ipt")
            ModlDir (string): directory with wind-independent files (e.g.,
                              Blade, Tower, Pitch files)
            FastDir (string): directory to write FAST & AeroDyn files to
            
        Keyword Args (dictionary):
            version (int): FAST version (7 or 8)
            verbose (boolean): flag to pring updates
            kwargs (dictionary): keyword arguments to WriteFastADOne [opt]
                 
    """
    
    if (version == 7):
        
        # define dictionary of default wind-dependent parameters
        WindDict = {'BlPitch(1)':0.,'BlPitch(2)':0.,'BlPitch(3)':0.,
                    'OoPDefl':0.,'IPDefl':0.,'TeetDefl':0.,'Azimuth':0.,
                    'RotSpeed':0.,'NacYaw':0.,'TTDspFA':0.,'TTDspSS':0.,
                    'TMax':630.,'TStart':30.,'WindFile':WindPath}
                    
        if verbose:
            print('\nWriting FAST v7.02 files for \"{:s}\" '.format(TurbName) + \
                    'with wind file {:s}...'.format(WindDict['WindFile']))
                
        # add passed-in arguments
        for key in kwargs:
            if key in WindDict.keys():
                WindDict[key] = kwargs[key]
        
        # check if IC look-up table exists...
        LUTPath = os.path.join(ModlDir,'steady_state',
                                          TurbName+'_SS.mat')
                                          
        #    if LUT exists, load unspecific IC values
        if os.path.exists(LUTPath):
            if verbose:
                print('  Interpolating unspecified IC values from ' + \
                        'look-up table {:s}'.format(LUTPath))
                    
            # get list of keys corresponding to initial conditions and LUT keys
            IC_keys  = GetICKeys(version)
            mdict    = scio.loadmat(LUTPath,squeeze_me=True)
            LUT_keys = [str(s).strip() for s in mdict['Fields']]
            LUT      = mdict['SS']
            
            # loop through IC keys
            for i_key in range(len(IC_keys)):
                IC_key = IC_keys[i_key]
                
                # if it's a blade pitch, different FAST key than LUT
                if ('BlPitch' in IC_key):
                    IC_key = 'BldPitch'                    
                    
                # see if IC key is in LUT, get LUT key if applicable
                try:
                    LUT_key = [s for s in LUT_keys if IC_key in s][0]
                except IndexError:
                    LUT_key = []
                
                # if IC was not passed in and key is in LUT
                if ((not [key for key in kwargs if IC_key in kwargs]) and \
                    LUT_key):
                        
                    # get grid-averaged first wind speed
                    u0 = jr_wind.GetFirstWind(WindDict['WindFile'])
                    
                    # linearly interpolate initial condition
                    IC = np.interp(u0,LUT[:,LUT_keys.index('WindVxi')],
                                        LUT[:,LUT_keys.index(LUT_key)])
                                        
                    # save initial condition
                    WindDict[IC_keys[i_key]] = IC
    
        # create and save filenames
        IntrDir    = os.path.join(ModlDir,'templates')       # Fast/AD template dir
        ADTempPath = os.path.join(IntrDir,TurbName+'_AD_template.ipt')
        ADName   = '{:s}_AD.ipt'.format(FastName)
        ADPath     = os.path.join(FastDir,ADName)
        FastName = '{:s}.fst'.format(FastName)
        FastTempPath = os.path.join(IntrDir,TurbName+'_template.fst')
        FastPath  = os.path.join(FastDir,FastName)
        
        WindDict['ADFile'] = os.path.join(FastDir,ADPath)
        
        
        # write AeroDyn file
        with open(ADTempPath,'r') as f_temp:
            with open(ADPath,'w') as f_write:
                for line in f_temp:
                    if ('{:' in line):
                        field = line.split()[1]
                        f_write.write(line.format(WindDict[field]))
                    else:
                        f_write.write(line)
                    
        # write FAST file
        with open(FastTempPath,'r') as f_temp:
            with open(FastPath,'w') as f_write:
                for line in f_temp:
                    if ('{:' in line):
                        field = line.split()[1]
                        f_write.write(line.format(WindDict[field]))
                    else:
                        f_write.write(line)
                        
    else:
        errStr = 'Code for FAST v8 has not yet been coded'
        ValueError(errStr)
                             
    return
    
def CreateFAST7Dict(FastPath,
                    save=0,save_dir='.',verbose=0):
    """ Build and save FAST 7 Python dictionary from input file
    
        Args:
            FastPath (string): path to .fst file
            
        Keyword Args:
            save (boolean): flag to save dictionary
            save_dir (string): directory for dictionary saving
            verbose (int): flag to suppress print statements
            
        Returns:
            TurbDict (dictionary): dictionary of turbine parameters
    """
    
    # ensure path is to a .fst file 
    if not FastPath.endswith('.fst'):
        err_str = 'Path {:s} is not to a FAST 7 input file'.format(FastPath)
        ValueError(err_str)
        
    # get turbine name and location, change to turbine directory
    turb_dir   = os.path.dirname(FastPath)
    fast_fname = os.path.basename(FastPath)
    
    if verbose:
        print('\nCreating FAST 7 dictionary...')
        print('  Reading FAST 7 file: {:s}'.format(fast_fname))
        print('  Directory:           {:s}'.format(turb_dir))
    
    # change to turbine directory, keep current directory
    old_dir = os.getcwd()
    os.chdir(turb_dir)
    
    # ====================== initialize dictionary ============================
    TurbDict = {}
    TurbDict['TurbName'] = fast_fname[:-4]
    TurbDict['TurbDir']  = turb_dir
    
    if verbose:
        print('\n  Processing files...')
        
    # ==================== read data from .fst file ===========================
        
# TODO: handle pitch.ipt if model actually uses DISCON controller
# TODO: add checks for TwrGagNodes and Bld  Gag nodes      
        
    if verbose:
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
        
    if verbose:
        sys.stdout.write('processed.\n')
            
    # ============== read data from platform file if used =====================
    if TurbDict['PtfmModel']:
        
        if verbose:
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
                
        if verbose:
            sys.stdout.write('processed.\n')
            
    # =================== read data from tower file ===========================
         
    if verbose:
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
            
    if verbose:
        sys.stdout.write('processed.\n')
                    
    # =============== read data from furling file if used =====================
    if ( TurbDict['Furling'] == 'True' ):
        
        if verbose:
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
                
        if verbose:
            sys.stdout.write('processed.\n')
            
    # =================== read data from blade files ==========================
                
    for i_bl in range(1,int(TurbDict['NumBl'])+1):
        
        # blade-specific keys
        bl_str = '_' + str(i_bl)                    # append '_x' to keys
        bl_key = 'BldFile({:d})'.format(i_bl)       # blade file key
        
        if verbose:
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
               
        if verbose:
            sys.stdout.write('processed.\n')
             
    # =================== read data from AeroDyn file =========================
        
    if verbose:
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
            line   = f.readline().split()[0].lstrip('\"').rstrip('\"\n')
            foilnm = line.split('/')[-1]
            foil_prop.append(foilnm)
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
        
    if verbose:
        sys.stdout.write('processed.\n')
                    
    # =============== read data from pitch file if used =====================
    if ( TurbDict['PCMode'] == 1):
        
# TODO: add check if pitch.ipt or DISCON
        TurbDict['PitchFile'] = 'pitch.ipt'
        
        if verbose:
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
                 
        if verbose:                   
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
    
def WriteFAST7Template(TurbDict,TmplDir,ModlDir,WrDir):
    """ Create turbine-specific FAST v7.02 template file.
        Template can then be used to write wind-file-specic .fst files.
    
        Args:
            TurbDict (dictionary): dictionary with FAST parameters
            TmplDir (string): directory with template files
            ModlDir (string): directory with wind-independent files (e.g.,
                              Blade, Tower, Pitch files)
            WrDir (string): directory to write Fast template to
        
    """

    TurbName     = TurbDict['TurbName']
    sys.stdout.write('\nWriting FAST 7.02 template for turbine {:s}...'.format(TurbName))
                        
    # define path to base template and output filename
    fpath_temp = os.path.join(TmplDir,'Template.fst')
    fpath_out  = os.path.join(WrDir,TurbName+'_template.fst')
    
    # get list of special .fst keys
    version, FastFlag = 7, 1
    windfile_keys = GetWindfileKeys(version,FastFlag) # skip -  depend on wind file
    inputfile_keys = GetInputFileKeys(version)        # add directory to fname
                    
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
                        value  = TurbDict[field]
                        
                        # if key is a used input file, add path to model directory
                        if ((field in inputfile_keys) and ('unused' not in value)):
                            value  = os.path.join(ModlDir,value)
                            
                        w_line = field.join([value_format.format(value),
                                            comment])
                    
                f_write.write(w_line)
# TODO: add check for proper tower/bladgagnde handling (currently does not do it right)  
             
    print('done.')
    
    return


def WriteAeroDynTemplate(TurbDict,TmplDir,ModlDir,AeroDir,WrDir):
    """ AeroDyn input file for FAST v7.02
    
        Args:
            TurbDict (dictionary): dictionary with FAST parameters
            TmplDir (string): directory with template files
            ModlDir (string): directory with wind-independent files (e.g.,
                              Blade, Tower, Pitch files)
            AeroDir (string): directory with aerodynamic files
            WrDir (string): directory to write Fast template to
    """
        
    TurbName     = TurbDict['TurbName']
    sys.stdout.write('\nWriting AeroDyn v13 template' + \
                        ' for turbine {:s}...'.format(TurbName))
                        
    # define path to base template and output filename
    fpath_temp = os.path.join(TmplDir,'Template_AD.ipt')
    fpath_out  = os.path.join(WrDir,TurbName + '_AD_template.ipt')
    
    # get list of keys to skip (they depend on wind file)
    version, FastFlag = 7, 0
    windfile_keys = GetWindfileKeys(version,FastFlag)
    
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
                        
                    # if foilnames, print them all with path to AeroDir
                    elif (field == 'FoilNm'):
                        FoilNames = TurbDict[field]
                        
                        # print first foilname manually
                        FoilPath  = os.path.join(AeroDir,FoilNames[0])
                        w_line    = field.join([value_format.format(FoilPath),
                                            comment])
                        f_write.write(w_line)        
                        
                        # loop through remaining airfoils
                        for i_line in range(1,len(TurbDict['FoilNm'])):
                            FoilPath  = os.path.join(AeroDir,FoilNames[i_line])
                            f_write.write('\"{:s}\"\n'.format(FoilPath))
                        w_line = ''
                        
                    # if AeroDyn schedule, print it
                    elif (field == 'ADSched'):      
                        
                        # loop through remaining airfoils
                        for i_line in range(0,len(TurbDict['ADSched'])):
                            w_line = value_format.format( \
                                        *TurbDict['ADSched'][i_line])
                            f_write.write(w_line + '\n')
                        w_line = ''
                    
                    #  if key is not to be skipped
                    elif (field not in windfile_keys):
# TODO: add try/except to load default value if field not in dictionary
                        value  = TurbDict[field]
                        w_line = field.join([value_format.format(value),
                                            comment])
                    
                f_write.write(w_line)
                
    print('done.')
    
    return


def WriteBladeFiles(TurbDict,TmplDir,WrDir):
    """ Blade input files for FAST v7.02
    
        Args:
            TurbDict (dictionary): dictionary with FAST parameters
            TmplDir (string): directory with template files
            WrDir (string): directory to write Fast template to
    """
        
    TurbName     = TurbDict['TurbName']
    print('\nWriting FAST v7.02 blade files for turbine {:s}...'.format(TurbName))
                        
    # define path to base template
    fpath_temp = os.path.join(TmplDir,'Template_Blade.dat')
    
    # loop through blades
    for i_bl in range(1,int(TurbDict['NumBl'])+1):
        
        sys.stdout.write('  Blade {:d}...'.format(i_bl))
    
        # get output paths and string appender for blade
        fname_out = TurbDict['BldFile({:d})'.format(i_bl)]
        fpath_out = os.path.join(WrDir,fname_out)
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


def WriteTowerFile(TurbDict,TmplDir,WrDir):
    """ Tower input files for FAST v7.02
    
        Args:
            TurbDict (dictionary): dictionary with FAST parameters
            TmplDir (string): directory with template files
            WrDir (string): directory to write Fast template to
    """
        
    TurbName     = TurbDict['TurbName']
    sys.stdout.write('\nWriting FAST v7.02 tower file for turbine {:s}...'.format(TurbName))
                        
    # define path to base template and output file
    fpath_temp = os.path.join(TmplDir,'Template_Tower.dat')
    fname_out = TurbDict['TwrFile']
    fpath_out = os.path.join(WrDir,fname_out)
    
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


def WritePitchCntrl(TurbDict,TmplDir,WrDir):
    """ Pitch control routine for Kirk Pierce controller for FAST v7.02
    
        Args:
            TurbDict (dictionary): dictionary with FAST parameters
            TmplDir (string): directory with template files
            WrDir (string): directory to write Fast template to
    """
        
    TurbName     = TurbDict['TurbName']
    sys.stdout.write('\nWriting FAST v7.02 pitch.ipt file for turbine {:s}...'.format(TurbName))
                        
    # define path to base template and output file
    fpath_temp = os.path.join(TmplDir,'Template_pitch.ipt')
    fname_out = TurbDict['PitchFile']
    fpath_out = os.path.join(WrDir,fname_out)
    
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
    
def GetWindfileKeys(version,FastFlag):
    """ List of keys that are windfile-specific
    
        Args:
            version (int): FAST version (7 or 8)
            FastFlag (int): AeroDyn (0) or FAST (1)
    
        Returns:
            windfile_keys (list): list of FAST keys that are windfile-specific
    """
    
    if version == 7:
        if FastFlag:
            windfile_keys = ['TMax','TStart',
                             'BlPitch(1)','BlPitch(2)','BlPitch(3)',
                             'OoPDefl','IPDefl','TeetDefl','Azimuth',
                             'RotSpeed','NacYaw','TTDspFA','TTDspSS',
                             'ADFile']
        else:
             windfile_keys = ['WindFile']
                 
    elif version == 8:
        errStr = 'Keys for FAST 8 have not been coded yet.'
        ValueError(errStr)
        
    else:
        errStr = 'Function only works for FAST v7 and v8.'
        ValueError(errStr)
    
    return windfile_keys
    
def GetInputFileKeys(version):
    """ List of keys in .fst that are input files
    
        Args:
            version (int): FAST version (7 or 8)
    
        Returns:
            inputfile_keys (list): list of FAST keys that are input files
    """
    
    if version == 7:
        inputfile_keys = ['DynBrkFi','PtfmFile',
                         'TwrFile','FurlFile','BldFile(1)',
                         'BldFile(2)','BldFile(3)','NoiseFile','ADAMSFile',
                         'LinFile']
                 
    elif version == 8:
        errStr = 'Keys for FAST 8 have not been coded yet.'
        ValueError(errStr)
        
    else:
        errStr = 'Uncoded version \"{:d}\".'.format(version)
        ValueError(errStr)
    
    return inputfile_keys
    
def GetICKeys(version):
    """ List of keys in .fst that are initial conditions
    
        Args:
            version (int): FAST version (7 or 8)
    
        Returns:
            IC_keys (list): list of FAST keys that are initial conditions
    """
    
    if version == 7:
        IC_keys = ['BlPitch(1)','BlPitch(2)','BlPitch(3)',
                        'OoPDefl','IPDefl','TeetDefl','Azimuth',
                        'RotSpeed','TTDspFA','TTDspSS']
                 
    elif version == 8:
        errStr = 'Keys for FAST 8 have not been coded yet.'
        ValueError(errStr)
        
    else:
        errStr = 'Uncoded version \"{:d}\".'.format(version)
        ValueError(errStr)
    
    return IC_keys
    
