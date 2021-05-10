#!/usr/bin/bash

#creating env variables
cwd="$(pwd)/torsion"

PDB="$(pwd)/pdb"
#server pdb
sPDB="/serv/data/pdb"
#goes here ....

CSV="$(pwd)/data"

script="$(pwd)/scripts"
a=0
#run pdbtorsions
for file in $sPDB/*.ent
do
    # a=$(($a+1))
    # if [ $a -eq 3 ]
    # then
    #     echo "a = $a"
    #     break
    # fi
    pdbtorsions $file > $cwd/`basename $file .pdb`.txt
done
#creat the csv output file 
for file in $cwd/*.txt
do
    echo "$file" | $script/./CisProline_ext.py >> $CSV/proline_dataset.csv
done