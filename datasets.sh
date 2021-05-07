#!/usr/bin/bash

#creating env variables
cwd="$(pwd)/torsion"

PDB="$(pwd)/pdb"

script="$(pwd)/scripts"

for file in $cwd/*.txt
do
    echo "$file" | $script/./CisProline_ext.py
done