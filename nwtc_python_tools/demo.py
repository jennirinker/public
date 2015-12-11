"""
Demonstration of Python tools for working with NWTC CAE tools:
    1) Create turbine dictionary from FAST file or load a pre-processed dict
    2) Write wind-independent, turbine-specific files
        - FAST template
        - AeroDyn template
        - Blade file(s)
        - Tower file
        - Pitch file (if PCMode = 1)
    3) Write wind-dependent files
        - FAST file
        - AeroDyn file
"""
import jr_fast, json

# ============================== user inputs ==================================

TurbDir    = 'demo_inputs/Turbine'              # directory to read turb files
WindDir    = 'demo_inputs/Wind'                 # directory to read wind files
WrDir      = '.'                                # directory to write files to
fast_fpath = TurbDir + '/WP0.75A08V00.fst'      # file to create dict from
DictPath = TurbDir + '/WP0.75A08V00_Dict.dat'   # path to load pre-processed
                                                # turbine dictionary
BlPitch0   = [2.6,2.6,2.6]      # opt: if None, autom. determined from windfile
RotSpeed0  = 12.1               # opt: if None, autom. determined from windfile
fileID     = '00'               # opt: wind-specific file identifier
TMax       = 100.               # opt: if None, set to max time in wind file

# flags to create turbine dictionary from .fst file or save dictionary
process_dict = 1     # 0: load saved dict, 1: process dict from .fst
save_dict    = 0     # 0: don't save processed dict

# =============== should not need to change below this line ===================

# create Python dictionary from .fst file (processes sub-files as necessary)
if process_dict:
    TurbDict = jr_fast.CreateFAST7Dict(fast_fpath,
                                       save=save_dict)

# alternatively, load a dictionary that already exists
else:
    with open(DictPath,'r') as f_dict:
        TurbDict = json.load(f_dict)

# write wind-dependent files (FAST and AeroDyn templates)
jr_fast.WriteFAST7Template(WrDir,TurbDict)
jr_fast.WriteAeroDynTemplate(WrDir,TurbDict)

# write wind-independent files (blade files, tower files, and pitch file)
jr_fast.WriteBladeFiles(WrDir,TurbDict)
jr_fast.WriteTowerFile(WrDir,TurbDict)
if (TurbDict['PCMode'] == 1):
    jr_fast.WritePitchCntrl(WrDir,TurbDict)

# write wind-dependent files (FAST and AeroDyn files) for all wind files in
#   specified directory
jr_fast.WriteFAST7InputsAll(TurbDir,TurbDict['TurbName'],WindDir,
                   BlPitch0=BlPitch0,RotSpeed0=RotSpeed0,
                   TMax=TMax,wr_dir=WrDir,TmplDir=WrDir)

print('\nDemo Script Complete.\n'.format(fast_fpath))
