#!/usr/bin/bash

for file in $(ls /home/eleanor/McAdam/*fits)
do 
	ls $(basename "${file}") > $(basename "${file%.fits}")_fitsfile.list
	echo Done ${file}
done

for FILE in $(ls /home/eleanor/McAdam/*fitsfile.list)
do
if [[ $(basename "${FILE}") == *"z0p45"* ]]; then
    RED_SHIFT=0.45
elif [[ $(basename "${FILE}") == *"z0p57"* ]]; then
    RED_SHIFT=0.57
elif [[ $(basename "${FILE}") == *"z0p70"* ]]; then
    RED_SHIFT=0.70
elif [[ $(basename "${FILE}") == *"z0p99"* ]]; then
    RED_SHIFT=0.99
elif [[ $(basename "${FILE}") == *"z1p16"* ]]; then
    RED_SHIFT=1.16
elif [[ $(basename "${FILE}") == *"z1p35"* ]]; then
    RED_SHIFT=1.35
elif [[ $(basename "${FILE}") == *"z1p56"* ]]; then
    RED_SHIFT=0.70
elif [[ $(basename "${FILE}") == *"z1p79"* ]]; then
    RED_SHIFT=0.70
elif [[ $(basename "${FILE}") == *"z2p05"* ]]; then
    RED_SHIFT=2.05
else
    echo "Redshift error"
fi
python ./python_scripts/mcadam_setup.py << EOF
${FILE}


y
1
y
4
y

n
n
3.2
1
${RED_SHIFT}
1
EOF
mv HPC_FILES $(basename ${FILE%.*})_HPC_FILES
done 
for d in ./*HPC* ;do [[ -d "$d" ]] && echo "${d##./}" >> dir_HPC.txt; done
python3 /home/eleanor/McAdam/1_run_mcadam_modify_HPC_files_script.py
for FOLDER in /home/eleanor/McAdam/*file_HPC_FILES/*
do 
if [[  "${FOLDER}" == *sim*sim*.MCINI ]]; then
    /home/eleanor/McAdam/McAdam_container/McAdam.sif NP ${FOLDER}
    #echo $FOLDER
fi
done
