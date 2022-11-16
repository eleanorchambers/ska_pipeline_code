# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 11:42:11 2022

@author: enorv
"""
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
''' 
This file takes in text files generated from running 'casa_task_script.py' and 
outputs plots of the results. 
'''
file_natural  = 'results_221001_01_natural.txt' #file to get data from
file_uniform  = 'results_221003_03_uniform.txt' #file to get data from
file_briggs_0  = 'results_221004_01_briggs_0.txt' #file to get data from
file_briggs_1  = 'results_221004_02_briggs_1.txt' #file to get data from
file_briggs_neg1  = 'results_221005_01_briggs_-1.txt' #file to get data from
def general(file, weighting):
    '''Step 1: get data'''
    def convert_data(file):
        '''all data as variables'''
        x = pd.read_csv(file, delimiter='\t')
        myuvfits = x["myuv.fits"]
        weight = x["weighting"] 	
        ms_file = x["my.ms"]	
        clean_threshold = x["threshold_val"]
        dirty_signal = x["signal dirty image"]
        clean_signal = x["signal clean image"]
        rms_dirty = x["RMS dirty image"]
        rms_clean = x["RMS clean image"]
        S_N_dirty = x["signal-noise (dirty)"]	
        S_N_clean = x["signal-noise (clean)"]	
        signal_position_clean = x["max_pos"]
        rms_clean_to = x["cleaned to RMS"]
        
        '''gets names to convert names to obervation times'''
        name_list = [name.replace('../sim_', '') for name in myuvfits]
        name_list = [name.replace('_', ' ') for name in name_list]
        name_list = [name.replace('rev.fits', ' ') for name in name_list]
        
        z = []
        HA = []
        hour = []
        orientation = []
        day = []
        for name in name_list:
            if name[0][:1] == '0':
                HA_i = 0.5
                day_i = float(name[4][:1])
                z_i = name[6:11]
                ori_i = name[12:14]
            else:
                HA_i = float(name[0][:1])
                day_i = float(name[2][:1])
                z_i = name[4:9]
                ori_i = name[10:12]
            hour_i = HA_i*2
            HA.append(HA_i)
            hour.append(hour_i)
            day.append(day_i)
            z.append(z_i)
            orientation.append(ori_i)
    
        z =[i.replace('z', '') for i in z]
        z =[i.replace('p', '.') for i in z]
        z =[float(i) for i in z]
        time = np.multiply(hour, day)
        
        S_N = x["signal-noise (clean)"] #signal to noise for all observation times and redshift
        
        '''function gets signal x,y position'''
        def get_signal_pos(signal_position_clean):
            pos_S_all = []
            for i in signal_position_clean:
                pos_S = i.replace("[", '')
                pos_S = pos_S.replace("]", '')
                pos_S = [int(num) for num in pos_S.split()]
                pos_S_all.append(pos_S)
            posSx = []
            posSy = []
            for l in  pos_S_all:
                    posSx.append(l[0])
                    posSy.append(l[1])
            return posSx, posSy
        posSx = get_signal_pos(signal_position_clean)[0]
        posSy = get_signal_pos(signal_position_clean)[1]
        
        redshift = np.array(z)
        signal_noise = np.array(S_N)
        observation_time = np.array(time)
        
        return name_list, redshift, observation_time, signal_noise, posSx, posSy, myuvfits
    '''function that allows 2 quantities to be obtained for 1 projection'''
    def sort_porjection_II(projection, name_list, quan1, quan2): 
        quant1_II = []
        quant2_II = []
        # quant3_II = []
        for i, j, k in zip(name_list, quan1, quan2):
            if projection in i:
                quant1_II.append(j)
                quant2_II.append(k)
                # quant3_II.append(l)
            else:
                # print('There was a projection input error for', i)
                pass
        return quant1_II, quant2_II
    
    '''this function writes sim names to re-image if signal is out of expected area'''
    def write_redo_names(posSx, posSy, myuvfits, file):
        fits_name = [name.replace('../', '') for name in myuvfits]
    
        for Sx, Sy, name in  zip(posSx, posSy, fits_name):
            if Sx <= 160 or Sx >= 210 and Sy <= 165 or Sy >= 230:
                with open(f'fits_redo_list_{file}.txt', 'a') as f:
                        f.write(name + '\n')
            else:
               pass
        return f'fits_redo_list_{file}'
    
    '''this function selects data based on observation time and adds to list'''
    def obs_by_time(time, redshift, signal_noise, observation_time, posSx_, posSy_, weighting, name_list):
        '''want this function to take in data and sort by obervation time'''
        # print(observation_time)
        # print(observation_time[0])
        # print(time)
        z = []
        SN = []
        posSx = []
        posSy = []
        obs_check = []
        name_list_out = []
        for i, j, k, l, m, n in zip(redshift, signal_noise, observation_time, posSx_, posSy_, name_list):
            if k == time: 
                z.append(i)
                SN.append(j)
                posSx.append(l)
                posSy.append(m)
                obs_check.append(k)
                name_list_out.append(n)
                # print(f'obs_time = {k}')
            else:
                # print(f'obs_time = {k}')
                pass
        # print(f'z={z}')
        good_z = []
        good_SN = []
        good_posSx = []
        good_posSy = []
        good_name_list = []
        bad_z = []
        bad_SN = []
        bad_posSx = []
        bad_posSy = []
        bad_name_list = []
        for i, j, k, Sx, Sy in zip(z, SN, name_list_out, posSx, posSy):
            if Sx <= 160 or Sx >= 210 and Sy <= 165 or Sy >= 230:
                bad_z.append(i)
                bad_SN.append(j)
                bad_posSx.append(Sx)
                bad_posSy.append(Sy) 
                bad_name_list.append(k)
            else:
                good_z.append(i)
                good_SN.append(j)
                good_posSx.append(Sx)
                good_posSy.append(Sy)
                good_name_list.append(k)
        # print(good_z)
        # print(bad_z)
        good_z_XY, good_SN_XY = sort_porjection_II('XY', good_name_list, good_z, good_SN)
        good_z_XZ, good_SN_XZ = sort_porjection_II('XZ', good_name_list, good_z, good_SN)
        good_z_YZ, good_SN_YZ = sort_porjection_II('YZ', good_name_list, good_z, good_SN)
        bad_z_XY, bad_SN_XY = sort_porjection_II('XY', bad_name_list, good_z, good_SN)
        bad_z_XZ, bad_SN_XZ = sort_porjection_II('XZ', bad_name_list, good_z, good_SN)
        bad_z_YZ, bad_SN_YZ = sort_porjection_II('YZ', bad_name_list, good_z, good_SN)
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H-%M-%S)")
        plt.figure()
        plt.plot(good_z_XY, good_SN_XY, 'o', color='#004600', label='XY')
        plt.plot(good_z_XZ, good_SN_XZ, 'D', color='#00de00', label='XZ')
        plt.plot(good_z_YZ, good_SN_YZ, 'P', color='#009200', label='YZ')
        plt.plot(bad_z_XY, bad_SN_XY, 'o', color='#720072', label='XY')
        plt.plot(bad_z_XZ, bad_SN_XZ, 'D', color='#be00be', label='XZ')
        plt.plot(bad_z_YZ, bad_SN_YZ, 'P', color='#ff00ff', label='YZ')
        plt.xlabel('redshift')
        plt.ylabel('S/N')
        plt.title(f'Plot for {time} hour observation (weighting={weighting})')
        plt.legend()
        plt.savefig(f'./plt_saves/Plot for {time} hour observation- weighting={weighting}_{timestampStr}.pdf', format='pdf') 
        return time, z, SN, posSx, posSy, obs_check
    '''this function selects data based on redshift and adds to list'''
    def obs_by_redshift(z_out, redshift, signal_noise, observation_time, posSx_, posSy_, weighting, name_list): 
        '''want this to be a function that can take values and sort the data by redshift'''
        z = []
        SN = []
        posSx = []
        posSy = []
        obs_time = []
        for i, j, k, l, m in zip(redshift, signal_noise, observation_time, posSx_, posSy_):
            if i == z_out: 
                z.append(i)
                SN.append(j)
                posSx.append(l)
                posSy.append(m)
                obs_time.append(k)
                # print(f'time = {k}')
            else:
                pass
        good_obs_time = []
        good_SN = []
        good_name_list = []
        good_posSx = []
        good_posSy = []
        bad_obs_time = []
        bad_SN = []
        bad_name_list = []
        bad_posSx = []
        bad_posSy = []
        # print(f'observation time = {obs_time}')
        for i, j, k, Sx, Sy in zip(obs_time, SN, name_list, posSx, posSy):
            if Sx <= 160 or Sx >= 210 and Sy <= 165 or Sy >= 230:
                bad_obs_time.append(i)
                bad_SN.append(j)
                bad_posSx.append(Sx)
                bad_posSy.append(Sy)
                bad_name_list.append(k)
            else:
                good_obs_time.append(i)
                good_SN.append(j)
                good_posSx.append(Sx)
                good_posSy.append(Sy)
                good_name_list.append(k)
        
        # print(f'good_obs_time = {good_obs_time}')
        good_obs_time_XY, good_SN_XY = sort_porjection_II('XY', good_name_list, good_obs_time, good_SN)
        good_obs_time_XZ, good_SN_XZ = sort_porjection_II('XZ', good_name_list, good_obs_time, good_SN)
        good_obs_time_YZ, good_SN_YZ = sort_porjection_II('YZ', good_name_list, good_obs_time, good_SN)
        bad_obs_time_XY, bad_SN_XY = sort_porjection_II('XY', bad_name_list, good_obs_time, good_SN)
        bad_obs_time_XZ, bad_SN_XZ = sort_porjection_II('XZ', bad_name_list, good_obs_time, good_SN)
        bad_obs_time_YZ, bad_SN_YZ = sort_porjection_II('YZ', bad_name_list, good_obs_time, good_SN)
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H-%M-%S)")
        figure = plt.figure()
        #for i, j, posSx, posSy in zip(obs_time, SN, posSx, posSy):
        plt.plot(good_obs_time_XY, good_SN_XY, 'o', color='#004600', label='XY')
        plt.plot(good_obs_time_XZ, good_SN_XZ, 'D', color='#00de00', label='XZ')
        plt.plot(good_obs_time_YZ, good_SN_YZ, 'P', color='#009200', label='YZ')
        plt.plot(bad_obs_time_XY, bad_SN_XY, 'o', color='#720072', label='XY')
        plt.plot(bad_obs_time_XZ, bad_SN_XZ, 'D', color='#be00be', label='XZ')
        plt.plot(bad_obs_time_YZ, bad_SN_YZ, 'P', color='#ff00ff', label='YZ')
        # plt.plot(good_obs_time, good_SN, '.', color='green')
        # plt.plot(bad_obs_time, bad_SN, '.',  color='m')
        plt.xlabel('observation time (hours)')
        plt.ylabel('S/N')
        plt.legend()
        plt.title(f'Plot for redshift of {z_out} (weighting={weighting})')
        plt.savefig(f'./plt_saves/Plot for redshift of {z_out}- weighting={weighting}_{ timestampStr}.pdf', format='pdf') 
        return z_out, z, SN, posSx, posSy, obs_time, figure
    
    
    
    
    data = convert_data(file) #data from file in usable form
    name_list = data[0]
    # projection = get_projection(name_list)
    # print(projection)
    redshift = data[1]
    observation_time = data[2]
    signal_noise = data[3]
    posSx = data[4]
    posSy = data[5]
    myuvfits = data[6]
    
    list_to_redo = write_redo_names(posSx, posSy, myuvfits, file) #write data to redo to txt file
    
    data_1hr = obs_by_time(1.0, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list) 
    data_4hr = obs_by_time(4.0, redshift, signal_noise, observation_time, posSx, posSy, weighting,  name_list)
    data_6hr = obs_by_time(6.0, redshift, signal_noise, observation_time, posSx, posSy, weighting,  name_list)
    data_8hr = obs_by_time(8.0, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_12hr = obs_by_time(12.0, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_18hr = obs_by_time(18.0, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    
    data_z0p45 = obs_by_redshift(0.45 , redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z0p57 = obs_by_redshift(0.57, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z0p70 = obs_by_redshift(0.70, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z0p99 = obs_by_redshift(0.99, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z1p16 = obs_by_redshift(1.16, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z1p35 = obs_by_redshift(1.35, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z1p56 = obs_by_redshift(1.56, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z1p79 = obs_by_redshift(1.79, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    data_z2p05 = obs_by_redshift(2.05, redshift, signal_noise, observation_time, posSx, posSy, weighting, name_list)
    return data_1hr, data_4hr, data_6hr, data_8hr, data_12hr, data_18hr, data_z0p45, data_z0p57,\
        data_z0p70, data_z0p99,data_z1p16,data_z1p35,data_z1p56, data_z1p79, data_z2p05, list_to_redo

natural_analysis = general(file_natural, 'natural')
uniform_analysis = general(file_uniform, 'uniform')
briggs_0_analysis = general(file_briggs_0, 'briggs, robust=0')
briggs_1_analysis = general(file_briggs_1, 'briggs, robust=1')
briggs_neg1_analysis = general(file_briggs_neg1, 'briggs, robust=-1')

