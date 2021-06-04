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




while getopts h:t:f:d:o: flag
do
    case "${flag}" in
        h) help_input="RUN";;
        t) torsion=${OPTARG};;
        f) fullname=${OPTARG};;
        d) DIR_name="${OPTARG}";;
        o) FILE_OUTPUT=${OPTARG};;
        
        [?]) printf >&2 "###############################################
###############################################
                        program: pdb_database_build \n \t\t\t by: Ayub Hareed \n flags: \n \t\t -t carries out pdbtorsion on pdb files \n \t\t -f pdb file  
                 -o [output name] output file for pdb list name \n
                 -d directory path where the pdb file is \n\n"; exit


    esac
done

if [[ $FILE_OUTPUT ]]
then 
    echo "File output : $FILE_OUTPUT";
else
    printf "\nNo file output name given for the preprocessed pdb_list \n\n"; exit
fi


# when -h flag is used the user guid text is printed ou
if [[ $help_input ]]
then 
    printf  "###############################################
###############################################
                        program: pdb_database_build \n flags: \n \t\t -t carries out pdbtorsion on pdb files \n \t\t -f pdb file  
                 -d directory path where the pdb file is \n\n"; exit
fi




echo "Age: $age";
echo "Full Name: $fullname";
#echo "directory: $DIR_name"




if [[ $DIR_name ]]
then
    echo "################################### $DIR_name"
    for file in $DIR_name/*.ent
    do
        pdbstatus=`checkpdb $file`
        pdb_name=`basename $file .pdb`
        echo "$pdb_name ################################"

        echo "$pdbstatus"
        okcheck="OK"
        echo "$okcheck"
        if [ "$pdbstatus" = "OK" ]
        then
            echo "The pdb $pdb_name is OK to use"
            rezpdb=`getresol $file | awk '{print $2}' | awk -F'/' '{print $1}'`
            # check if its less than 3
            REZ=`echo $rezpdb '<=' 3.00 | bc -l`

            if [ "$REZ" -eq "1" ]
            then
                echo "$pdb_name has resolution of $REZ "
                echo -n " $pdb_name" >> $FILE_OUTPUT
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