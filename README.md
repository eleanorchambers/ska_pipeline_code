# Order of file use:

1. Make .cmd files using:
    - build_profile_scripts.py
    - simulation example.txt
    - YMAP filenames.txt
2. Make simulations using profile:
    - modify the 'run_profile.sh' to have correct paths etc
    - run run_profile.sh
3. Inverse fits files to import to CASA using:
    - inverse_fits_to_import_casa.py
4. Make and clean images in CASA using: 
    - casa_task_script.py
5. Read and plot results from 4. using:
    - read_and_plot_results.py
6. Do uv binning for McAdam:
    - uv_binning.sh
7. Make models with McAdam using:
    - run 0_all_run_mcadam.sh
    - 0_all_run_mcadam.sh uses 1_run_mcadam_modify_HPC_files_script.py
8. Make .cmd files for McAdam model clusters using:
    - build_profile_scripts_mcadam.py
    - simulation example_mcadam.txt
    - YMAP filenames.txt
9. Make simulations using profile:
    - modify the 'run_profile.sh' to have correct paths etc
    - run run_profile.sh
10. Remove model simulation from original cluster simulation to import to CASA:
    - remove_cluster_to_import_casa.py
11. Make and clean images in CASA using: 
    - casa_task_script_substructure.py
    - use this ^ file as it has no mask

### Other Files: 

- casa_import_ymaps.py can be run in CASA to import ymaps as images to be viewed
- correct_coordinates.py and ymap_images.txt can be used to correct the ymap image coordinates to match that of the simulations

Email enorvw@gmail.com for any questions. 