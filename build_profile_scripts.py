"This script is designed to generate .cmd files to make simulations with profile"

#files needed
sample_filename = 'simulation example.txt' #sample file that contains information to be copied to written to the new files
ymap_names_file = 'YMAP filenames.txt' #text file of ymap filenames

#observations to make
HA = '4'
days = '1'
integration_time = '55'
    
    
#observation inputs 
def _get_lines_(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines
"this function chooses the correct cellsize based on the filename"
def _cell_size_(filename): 
    # replace = {'p45':'2.000960825', 'p57':'2.001172081', etc etc etc}
    # replacement = replace[filename]
    #the if statements selects the correct replacement
    if 'p45' in filename:
        replacement = '2.000960825'
    elif 'p57' in filename:
        replacement = '2.001172081'
    elif 'p70' in filename:
        replacement = '2.001377716'
    elif 'p99' in filename:
        replacement = '2.001765663'
    elif 'p16' in filename:
        replacement = '2.001945594'
    elif 'p35' in filename:
        replacement = '2.002115134'
    elif 'p56' in filename:
        replacement = '2.002273889'
    elif 'p79' in filename:
        replacement = '2.002421732'
    elif 'p05' in filename:
        replacement = '2.002558748'
    else:
        print('Error in new filename')
    #these next steps gets the file contents, replaces the cellsize with correct replacement
    #then writes to the same file
    with open(filename, 'r') as f:
        contents = f.read()
    contents = contents.replace('cellsize', replacement)
    with open(filename, 'w') as f: 
        f.write(contents)
def YMAP_no(filename):
     if 'p45' in filename:
         return 'z0p45'
     elif 'p57' in filename:
         return 'z0p57'
     elif 'p70' in filename:
         return 'z0p70'
     elif 'p99' in filename:
         return'z0p99'
     elif 'p16' in filename:
         return 'z1p16'
     elif 'p35' in filename:
         return 'z1p35'
     elif 'p56' in filename:
         return 'z1p56'
     elif 'p79' in filename:
         return 'z1p79'
     elif 'p05' in filename:
         return 'z2p05'
     else:
         print('redshift name error')  
def orientation(ymap_names):
    
         if 'XY' in ymap_names:
             return 'XY'
         elif 'XZ' in ymap_names:  
             return 'XZ'
         elif 'YZ' in ymap_names:
             return 'YZ'
         else:
             print('orinentation name error')  
             
def _dup_filename_(ymap_names_file, HA, days): 
        ymap_names = _get_lines_(ymap_names_file)
        
        YMAP_no_list = []
        for name in ymap_names: 
            YMAP_number = YMAP_no(name)
            YMAP_no_list.append(YMAP_number)
            
        orientation_list = []
        for name in ymap_names: 
            o = orientation(name)
            orientation_list.append(o)
        
        dup_filename_list = ['sim_'+ HA + '_' + days + '_' + i + '_' + j + '.cmd' for i, j in zip(YMAP_no_list, orientation_list)]
        #dup_filename_list = [f'sim_{HA}_{days}_' + i + '_' + j + '.cmd' for i, j in zip(YMAP_no_list, orientation_list)]

        return dup_filename_list
    
def _ymap_path_list_(ymap_names_file): 
    ymap_names = _get_lines_(ymap_names_file)
    path_list = ['./ymaps/' + name for name in ymap_names]
    return path_list
    
def _ymap_path_(path_name, file):
    with open(file, 'r') as f:
            contents = f.read()
    contents = contents.replace('YMAP.fits', path_name.strip())
    with open(file, 'w') as f: 
            f.write(contents)    
            
def _replace_vars_(HA, days, file):
   
    name = file.replace('.cmd', '')
    with open(file, 'r') as f:
        contents = f.read()
    contents = contents.replace('HA', HA)
    contents = contents.replace('days', days)
    contents = contents.replace('SIM_OBS', name, 1)
    contents = contents.replace('name', name, 1)
    contents = contents.replace('integration_time', integration_time)
    with open(file, 'w') as f: 
        f.write(contents)

def _make_copy_(sample_filename, dup_filename):
    with open(sample_filename, 'r') as rf: 
        with open(dup_filename, 'w') as wf:
            for line in rf:
                wf.write(line)
    return dup_filename

new_files_names = _dup_filename_(ymap_names_file, HA, days)
ymap_path_list = _ymap_path_list_(ymap_names_file)


for i, j in zip(new_files_names, ymap_path_list):
        file = _make_copy_(sample_filename, i)
        cellsize = _cell_size_(file)
        replace_vars = _replace_vars_(HA, days, file)
        ymap_path = _ymap_path_(j, file)
        

