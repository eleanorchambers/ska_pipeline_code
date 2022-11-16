'''This file imports ymaps as images in casa'''
def _get_lines_(filename):
    lines = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines
    
def _fits_file_list_(fits_filenames_txt): 
    fits_filenames = _get_lines_(fits_filenames_txt)
    path_list = ['../' + 'ymaps/' + name.strip() for name in fits_filenames]
    return path_list
    
myuv_fits = _fits_file_list_('../ymaps/YMAP filenames.txt') #must be string also, hopefully designed to be a list that is iterated over
#myuv_fits = ['../ymaps/Maps_z0p45_halo_0010-Ysz-XY_ymap.fits'] #trial map import

for file in myuv_fits:

    base_name = file.replace('../', '')
    base_name = base_name.replace('.fits', '')
    base_name = base_name.replace('ymaps/', '')
    
    my_image = base_name + '.image' #want this file to correspond to uvfits file name
    
    if os.path.isfile(my_image):
    	pass
    else:
    	importfits(str(file), str(my_image)) #imports fits file to image file
