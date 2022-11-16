'''I want this task to:
        1. import fits files
        2. create dirty image using clean
        3. read noise + signal from dirty image
        4. write those measurements to file
        5. use noise measurement to create clean image
        6. get second signal to noise measurement 
        
        Also want to be able to specify weighting for each clean, and threshold for clean image'''

'''Instructions: input variables to casa, ie results_txt = 'xxx', weighting = 'xxx'. 
		Put fits file names into txt file called fits_filenames_model.txt
        
        Note: weighting must be: uniform, natural, or briggs. If briggs, must also also set 
        robust_var = number (the number must belong to: [-2, 2])
        As it is set up currently, results will be fed into a folder called 'data_clean_results_files'
        And ms files and images will be saved to a folder called 'data_clean_results_files'
        
        Note: this is a modified version of the 'casa_task_script.py' without a mask to 
        clean images to investigate cluster substructures.
'''

import os.path

def main():
    results_name = results_txt
    weight = weighting #must be string 'natural', 'uniform', 'briggs'
    
    if weight == 'natural': #need to figure out how to do what I actually want here before uncommenting
    	pass
    elif weight == 'briggs':
    	pass
    elif weight == 'uniform':
    	pass
    else:
    	print('weighting error')
    	return
    
    if weight == 'briggs':
    	robust = robust_var
    else:
    	pass
    
    def _get_lines_(filename):
        lines = []
        with open(filename, 'r') as f:
            lines = f.readlines()
        return lines
        
    def _fits_file_list_(fits_filenames_txt): 
        fits_filenames = _get_lines_(fits_filenames_txt)
        path_list = ['../' + name.strip() for name in fits_filenames]
        return path_list
        
    myuv_fits = _fits_file_list_('../fits_filenames_model.txt') #must be string also, hopefully designed to be a list that is iterated over
    
    
    filename = './data_clean_results_files/' + results_name
    headers = 'myuv.fits'+ '\t' +'weighting'+ '\t' +'my.ms'+ '\t' +'threshold_val'+ '\t' +'signal dirty image'+ '\t' +'signal clean image'+ '\t' +'RMS dirty image'+ '\t' +'RMS clean image'+ '\t' +'signal-noise (dirty)'+ '\t' +'signal-noise (clean)'+ '\t' +'max_pos'+ '\t' +'cleaned to RMS'
    with open(filename, 'a') as f: #appends all values from cleaning to file
        f.write(str(headers))
        
        
    for file in myuv_fits:
    
        base_name = file.replace('../', './data_storage_for_cleans/')
        base_name = base_name.replace('.fits', '')
        
        my_ms = base_name + '.ms' #want this file to correspond to uvfits file name
        
        if os.path.isdir(my_ms): #this is not working properly... fix later
        	pass
        else:
        	importuvfits(fitsfile= str(file), vis= str(my_ms)) #imports fits file to ms file
        	
        	
        if weight == 'briggs': 
        	weight_name = str(weight) + '_' + str(robust)
        else: 
        	weight_name = weight
        	
        im_name_d = base_name + '_dirty_' + weight_name
        
        clean(vis = my_ms, imagename = im_name_d, uvrange = '<10000lambda', imsize= [384], cell=["3arcsec"], weighting=weight, niter=0)
        
        im_dirty = base_name + '_dirty_' + weight_name + '.image'
        stats_dirty_S = imstat(im_dirty, region= 'circle[[01h00m00s, -30.00.00.000], 33.5arcsec]' ) #want min value only from middle region to avoid picking something that isn't the signal 
        stats_dirty_N = imstat(im_dirty) #get noise from whole image
        
        signal_d = stats_dirty_S['max'][0] #signal from region to be masked
        rms_d = stats_dirty_N['rms'][0] #rms from whole image
        S_N_d = abs(signal_d)/rms_d
        
        clean_level = 1
        threshold_val = str((clean_level*rms_d)/(1e-6)) + 'uJy'
        
        im_name_c = base_name + '_clean_' + weight_name
        
        clean(vis= my_ms, imagename=im_name_c, uvrange='<10000lambda', imsize=[384], cell=["3arcsec"], weighting=weight, niter=2000, threshold= threshold_val, mask= 'circle[[01h00m00s, -30.00.00.000], 45arcsec]')
        
        im_clean = base_name + '_clean_' + weight_name + '.image' #clean image name
        res_clean = base_name + '_clean_' + weight_name + '.residual' #clean image residual, want RMS from here
        
        stats_clean_im = imstat(im_clean)
        stats_clean_res = imstat(res_clean)
        
        signal_c = stats_clean_im['max'][0]
        rms_c = stats_clean_res['rms'][0]
        S_N_c = abs(signal_c)/rms_c
        
        clean_max_pos = stats_clean_im['maxpos']
        print(clean_max_pos)
        
        
        values_list =  str(file)+ '\t' +str(weight_name)+ '\t' +str(my_ms)+ '\t' +str(threshold_val)+ '\t' +str(signal_d)+ '\t' +str(signal_c)+ '\t' +str(rms_d)+ '\t' +str(rms_c)+ '\t' +str(S_N_d)+ '\t' +str(S_N_c).strip()+ '\t' +str(clean_max_pos)+ '\t' +str(clean_level)
        
        with open(filename, 'a') as f: #appends all values from cleaning to file
            f.write('\n'+ values_list)
        
    #region= 'circle[[01h00m00s, -29.59.56.524], 33.5arcsec]'  #region used in imstat dirty image
    #mask= 'circle[[01h00m00s, -29.59.56.524], 33.5arcsec]' #mask for cleaning central region


main()
