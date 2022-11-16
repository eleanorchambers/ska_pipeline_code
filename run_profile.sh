#!/usr/bin/bash

for FILE in $(ls /home/eleanor/sim*.cmd)
do
./profile.sif <<EOF
yes
no
run $FILE
exit
y
EOF
done
