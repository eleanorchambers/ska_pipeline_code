#!/usr/bin/bash


for filename in /home/eleanor/Simulations/Original_fits/*.fits ; do
	python ./python_scripts/uvsep.py --inputfile=$filename --outroot=$(basename "$filename" .fits) --uvbin --uvcut=10000 
	done

