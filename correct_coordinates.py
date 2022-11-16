
def _get_lines_(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines   

def image_file_list_(image_filenames_txt): 
    image_filenames = _get_lines_(image_filenames_txt)
    path_list = ['/home/eleanor/Casa/Ymap images/' + name.strip() for name in image_filenames]
    return path_list


crval1=imhead('/home/eleanor/Casa/data_storage_for_cleans/sim_3_3_z0p57_XY_mod_rem_clean_natural.image', mode='get', hdkey='crval1') 
crval2=imhead('/home/eleanor/Casa/data_storage_for_cleans/sim_3_3_z0p57_XY_mod_rem_clean_natural.image', mode='get', hdkey='crval2') 
  
ymap_images = image_file_list_('/home/eleanor/Casa/Ymap images/ymap_images.txt')

print(ymap_images)

for i in ymap_images:
	imhead(i, mode='put', hdkey='crval1', hdvalue=crval1)
	imhead(i, mode='put', hdkey='crval2', hdvalue=crval2) 


