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
import jr_fast, json, os

# ============================== user inputs ==================================

# flags to create turbine dictionary from .fst file or save dictionary
process_dict = 1     # 0: load saved dict, 1: process dict from .fst
save_dict    = 0     # 0: don't save processed dict

# simulation specifications
SimSpecs = {'BlPitch(1)':2.6,'BlPitch(2)':2.6,'BlPitch(3)':2.6,
            'RotSpeed':12.1,'TMax':630.,'TStart':30.}
            
# directories and filepaths (shouldn't need to change for demo)
CWD     = os.getcwd()                       # current working directory
TmplDir = os.path.join(CWD,'templates')     # loc of all template files
ModlDir = os.path.join(CWD,'demo_outputs')  # loc of blade, pitch, tower files
                                            #    and directory with inter- 
                                            #    mediate FAST/AD templates
FastDir = os.path.join(CWD,'demo_outputs')  # loc of final FAST/AD files
WindDir = os.path.join(CWD,'demo_inputs',
                          'Wind')           # loc of wind files
AeroDir = os.path.join(CWD,'demo_inputs',
                       'AeroData')          # loc of airfoil data
ReadDir  = os.path.join(CWD,'demo_inputs',
                        'Turbine')         # loc pre-made FAST files to read
FastPath = os.path.join(ReadDir,
                        'WP0.75A08V00.fst')       # file to create dict from
DictPath = os.path.join(ReadDir,
                        'WP0.75A08V00_Dict.dat')  # path to pre-processed
                                                  # turbine dictionary

# =============== should not need to change below this line ===================

# create Python dictionary from .fst file (processes sub-files as necessary)
if process_dict:
    TurbDict = jr_fast.CreateFAST7Dict(FastPath,
                                       save=save_dict)

# alternatively, load a dictionary that already exists
else:
    with open(DictPath,'r') as f_dict:
        TurbDict = json.load(f_dict)

# write templates for files that depend on wind file (FAST and AeroDyn)
jr_fast.WriteFAST7Template(TurbDict,TmplDir,ModlDir)
jr_fast.WriteAeroDynTemplate(TurbDict,TmplDir,
                             ModlDir,WindDir,AeroDir)

# write wind-independent files (blade files, tower files, and pitch file)
jr_fast.WriteBladeFiles(TurbDict,TmplDir,ModlDir)
jr_fast.WriteTowerFile(TurbDict,TmplDir,ModlDir)
if (TurbDict['PCMode'] == 1):
    jr_fast.WritePitchCntrl(TurbDict,TmplDir,ModlDir)

# write wind-dependent files (FAST and AeroDyn files) for all wind files in
#   specified directory
jr_fast.WriteFastADAll(TurbDict['TurbName'],ModlDir,WindDir,FastDir,
                            Naming=2,**SimSpecs)

print('\nDemo Script Complete.\n')


