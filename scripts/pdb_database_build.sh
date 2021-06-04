#! /usr/bin/bash

#*************************************************************************
#
#   Program:    pdb_database_build
#   File:       pdb_database_build.sh
#
#   Version:    V1.0
#   Date:       03.06.21
#   Function:   uses multiple programs such as: 
#                -- checkpdb: which checks if a pdb file doesn't have
#                            missing residues 
#
#                -- getresol: returns the resolution of a pdb file
#
#                --  
#
#               prints out a list of pdb names that have filtered for resolution
#               less than or equal to 3.00A and no missing residues.
#
#
#   Author:     Ayub Hareed
#
#   EMail:      ayubm56@gmail.com
#
#
#*************************************************************************
#
#   Description:
#   ============
#
#*************************************************************************
#
#   Usage:
#   ======
#
#*************************************************************************
#
#   Revision History:
#   =================
#   V1.0   03.06.21  Original   By: Ayub Hareed
#**************************************************************************


##declare -a ourlsts=(`./remove_missing_res.py`)

# assigning the command line arguments




while getopts h:t:f:d: flag
do
    case "${flag}" in
        h) username=${OPTARG};;
        t) age=${OPTARG};;
        f) fullname=${OPTARG};;
        d) DIR_name="${OPTARG}";;
        [?]) printf >&2 "###############################################
###############################################
                        program: pdb_database_build \n flags: \n \t\t -t carries out pdbtorsion on pdb files \n \t\t -f pdb file  
                 -d directory path where the pdb file is \n\n"; exit

    esac
done

if [[ $username ]]
then 
    echo "Username: $username";
fi

echo "Age: $age";
echo "Full Name: $fullname";
#echo "directory: $DIR_name"




if [[ $DIR_name ]]
then
    echo "################################### $DIR_name"
    for file in $DIR_name/*.pdb
    do
        pdbstatus=`checkpdb $file`
        pdb_name=`basename $file .pdb`
        echo "$pdb_name ################################"

        echo "$pdbstatus"
        okcheck="OK"
        echo "$okcheck"
        if [ "$pdbstatus" = "OK" ]
        then
            echo "The pdb 2h03 is OK to use"
            rezpdb=`getresol $file | awk '{print $2}' | awk -F'/' '{print $1}'`
            # check if its less than 3
            REZ=`echo $rezpdb '<=' 3.00 | bc -l`

            if [ "$REZ" -eq "1" ]
            then
                echo "it works"
                echo -n " $pdb_name" >> pdb_list.txt
            fi

        fi
    done


fi
echo "start code"

# for i in "${ourlsts[@]}"
# do 
#     echo "$i"
# done
   

#rezpdb=`getresol /home/ayubh/project/git_clone/cis-proline-pred/pdb/2wek.pdb | awk '{print $2}' | awk -F'/' '{print $1}'`