"""
Demonstration of Python tools for working with NWTC CAE tools:
    1) Create turbine dictionary from FAST file
    2) Write turbine-specific .fst template
"""
import jr_fast,os

# ============================== user inputs ==================================

# specify path to FAST file to create dictionary from
fast_fpath = os.path.join('demo_inputs','WP0.75A08V00.fst')

# directory to write FAST files to
wr_dir = 'demo_outputs'

# =============== should not need to change below this line ===================

# create Python dictionary from FAST file
TurbDict = jr_fast.CreateFAST7Dict(fast_fpath)

# write wind-dependent files (FAST and AeroDyn templates)
jr_fast.WriteFAST7Template(wr_dir,TurbDict)
jr_fast.WriteAeroDynTemplate(wr_dir,TurbDict)

# write wind-independent files (blade files, tower files, and pitch file)
jr_fast.WriteBladeFiles(wr_dir,TurbDict)
jr_fast.WriteTowerFile(wr_dir,TurbDict)
if (TurbDict['PCMode'] == 1):
    jr_fast.WritePitchCntrl(wr_dir,TurbDict)

print('\nScript Complete.\n'.format(fast_fpath))
