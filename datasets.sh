#!/usr/bin/bash

#creating env variables
cwd="$(pwd)/torsion"

PDB="$(pwd)/pdb"
#server pdb
sPDB="/serv/data/pdb"

#run pdbtorsions
for file in $sPDB/*.ent
do
    pdbtorsions $file > $cwd/`basename $file .ent`.txt
done

