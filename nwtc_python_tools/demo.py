"""
Demonstration of Python tools for working with NWTC CAE tools:
    1) Create turbine dictionary from FAST file
    2) Write turbine-specific .fst template
    3) Wrtte 
"""
import jr_fast,os

# specify path to FAST file
fast_fpath = os.path.join('demo_inputs','WP0.75A08V00.fst')

print('\nCreating dictionary for turbine {:s}...\n'.format(fast_fpath))

# create Python dictionary from FAST file
turb_dict = jr_fast.CreateFAST7Dict(fast_fpath)

print('Writing .fst template...\n'.format(fast_fpath))

# write turbine-specific fast and aerodyn templates
fpath_out = '.'
jr_fast.WriteFASTTemplate(fpath_out,turb_dict)

print('Script complete.\n'.format(fast_fpath))
