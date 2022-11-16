from astropy.io import fits
import os 

def _get_lines_(filename):
        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        return lines
        
def _fits_file_list_(fits_filenames_txt): 
	fits_filenames = _get_lines_(fits_filenames_txt)
	path_list = ['./' + name.strip() for name in fits_filenames]
	return path_list
        
#my_files = _fits_file_list_('./og_fits_filenames.txt') #must be string also, hopefully designed to be a list that is iterated over
model_sims = _fits_files_list_('./model_sim_filenames.txt')
rev_fits = _fits_file_list_('./rev_fits_filenames.txt')


for model, rev in zip(model_sim, rev_fits):

	model_subtracted = model.replace('.fits', '_rem.fits')
	model_subtracted = '/media/eleanor/T7 Shield/1. Phys417 Project Files/Removing_model/' + model_subtracted
	
	if os.path.isfile(model_subtracted):
		pass
	else:
		f=fits.open(rev) 
		f2=fits.open(model) 
		f[0].data.data[...,0]+=f2[0].data.data[...,0] 
		f[0].data.data[...,1]+=f2[0].data.data[...,1] 
		f.verify('fix') 
		f.writeto(model_subtracted) 
		


	



