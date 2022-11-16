"This script is set up to be run in /home/eleanor/McAdam"

HPC_FOLDERS_list = "dir_HPC.txt"
include_file_og = "INCLUDE_FILE.MCINI"

def get_lines_(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines
    
def make_copy_(include_file, include_new):
    with open(include_file, 'r') as rf: 
        with open(include_new, 'w') as wf:
            for line in rf:
                wf.write(line)
    return include_new

def replace_vars_O(cp_include_file, folder):
    chains_path = "/home/eleanor/McAdam/chains"
    with open(cp_include_file, 'r') as f:
        contents = f.read()
    contents = contents.replace("! Joint 2D elliptical Gaussian prior in log-space\n        Gas_PriorType(1,1) = 14\n        Gas_Prior(1,1) = 0.6171, 0.1153, 0.7011         !thetas_Planck(arcmin)\n        Gas_PriorType(1,2) = 14\n        Gas_Prior(1,2) = -2.743, 0.2856, 0.7011         !Ytot_Planck (arcmin2)", "! Joint 2D elliptical Gaussian prior in log-space\n        Gas_PriorType(1,1) = 1\n        Gas_Prior(1,1) = 0.083333, 10         !thetas_Planck(arcmin)\n        Gas_PriorType(1,2) = 1\n        Gas_Prior(1,2) = 1d-3, 0.1         !Ytot_Planck (arcmin2)")
    contents = contents.replace('cell=30.0', 'cell=5.0 \n      thetas_hardlim=0d0') 
    contents = contents.replace('DATADIR', f'/home/eleanor/McAdam/{folder}')
    contents = contents.replace('IncludeCMB=1', 'IncludeCMB=0')
    contents = contents.replace('nest_nlive=100', 'nest_nlive=200')
    contents = contents.replace('OUTDIRECTORY', f'{chains_path}/{simname}_O')
    with open(cp_include_file, 'w') as f: 
        f.write(contents)
        
def replace_vars_O_P(cp_include_file, folder):
    chains_path = "/home/eleanor/McAdam/chains"
    with open(cp_include_file, 'r') as f:
        contents = f.read()
    contents = contents.replace('SamplePrior = F', 'SamplePrior = T')
    contents = contents.replace('nest_nlive=200', 'nest_nlive=1000')
    contents = contents.replace(f'{chains_path}/{simname}_O', f'{chains_path}/{simname}_O_P')
    with open(cp_include_file, 'w') as f: 
        f.write(contents)

def replace_vars_O_N(cp_include_file, folder):
    chains_path = "/home/eleanor/McAdam/chains"
    with open(cp_include_file, 'r') as f:
        contents = f.read()
    contents = contents.replace("! Joint 2D elliptical Gaussian prior in log-space\n        Gas_PriorType(1,1) = 1\n        Gas_Prior(1,1) = 0.083333, 10         !thetas_Planck(arcmin)\n        Gas_PriorType(1,2) = 1\n        Gas_Prior(1,2) = 1d-3, 0.1         !Ytot_Planck (arcmin2)", "! Joint 2D elliptical Gaussian prior in log-space\n        Gas_PriorType(1,1) = 1\n        Gas_Prior(1,1) = 0.083333, 10         !thetas_Planck(arcmin)\n        Gas_PriorType(1,2) = 0\n        Gas_Prior(1,2) = 0, 0, 0         !Ytot_Planck (arcmin2)")
    contents = contents.replace(f'{chains_path}/{simname}_O', f'{chains_path}/{simname}_O_N')
    with open(cp_include_file, 'w') as f: 
        f.write(contents)

HPC_FOLDERS_list = get_lines_(HPC_FOLDERS_list)

for folders in HPC_FOLDERS_list: 
	simname = folders.strip().replace('_fitsfile_HPC_FILES', '')
	print(f'simname={simname}')
	include_new = simname.replace(f'{simname}', f'{simname}_O.MCINI')
	print(f'include_new={include_new}')
	include_path = folders.strip()
	print(f'include_path={include_path}')
	include_file = f'{include_path}/{include_file_og}'
	include_new = make_copy_(include_file, f'{include_path}/{include_new}')
	#print(include_new)
	include_new = replace_vars_O(include_new, include_path)
	new_copy_files = simname.replace(f'{simname}', f'{simname}_O.MCINI')
	new_copy_files = f'{include_path}/{new_copy_files}'
	print(f'new file to copy = {new_copy_files}')
	prior_include = simname.replace(f'{simname}', f'{simname}_O_P.MCINI')
	prior_include = make_copy_(new_copy_files, f'{include_path}/{prior_include}')
	prior_include = replace_vars_O_P(prior_include, include_path)
	null_include = simname.replace(f'{simname}', f'{simname}_O_N.MCINI')
	null_include = make_copy_(new_copy_files, f'{include_path}/{null_include}')
	null_include = replace_vars_O_N(null_include, include_path)
	
	
	
	
