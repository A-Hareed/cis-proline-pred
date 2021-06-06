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




while getopts h:t:f:d:o:e:p:x: flag
do
    case "${flag}" in
        h) help_input="RUN";;
        t) torsion=${OPTARG};;
        f) fullname=${OPTARG};;
        d) DIR_name="${OPTARG}";;
        o) FILE_OUTPUT=${OPTARG};;
        e) EXTENSION=${OPTARG};;
        p) PDBDATA=${OPTARG};;
        x) ENCODER=${OPTARG};;
        
        [?]) printf >&2 "###############################################
###############################################
                        program: pdb_database_build \n \t\t\t by: Ayub Hareed \n flags: \n \t\t -t [OUTPUT path] carries out pdbtorsion on pdb files \n \t\t -f pdb file  
                 -o [output name] output file for pdb list name \n
                 -e [pdb file prefix] used to loop through pdb file prefix e.g. '.ent' \n
                 -d directory path where the pdb file is \n\n"; exit


    esac
done

# if [[ $FILE_OUTPUT ]]
# then 
#     echo "File output : $FILE_OUTPUT";
# else
#     printf "\nNo file output name given for the preprocessed pdb_list \n\n"; exit
# fi

echo "####exporting weka#######"
export WEKA=/nas/backup/work/newserver/bsmhome/zcbthhn/weka-3-8-3
export CLASSPATH="$WEKA/weka.jar"
export CLASSIFIER=weka.classifiers.functions.MultilayerPerceptron

if [[ $EXTENSION ]] && [[ $EXTENSION != "*"  ]]
then 
    echo "PDB File EXTENSION : $EXTENSION";

elif [[ $EXTENSION = "*" ]]
then 
    echo "extension is : $EXTENSION"
    EXTENSION=" "
else
    EXTENSION='.ent'
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
culled_pdb_array=(`/home/ayubh/project/git_clone/cis-proline-pred/scripts/getpdb.py $PDBDATA`)

CURRENT_DIRECTORY=`pwd`
echo "####################################################"
echo "the current working directory is: $CURRENT_DIRECTORY"
echo "####################################################"
echo "####################################################"

if [[ $DIR_name ]]
then
#     echo "################################### $DIR_name"
#     for file in $DIR_name/*$EXTENSION
#     do
#         #pdbstatus=`checkpdb $file`
#         pdb_name=`basename $file $EXTENSION`
#         echo "################## $pdb_name ################################"

#         echo "$pdbstatus"
#         okcheck="OK"
        
#         #if [ "$pdbstatus" = "OK" ]
    for culled_pdb in ${culled_pdb_array[@]}
    do
        echo "$culled_pdb"
        pdb_name_file=$DIR_name/${culled_pdb}.ent
        # if [ [$culled_pdb = $pdb_name ] ]
        # then
        echo "The pdb $pdb_name is equal to $culled_pdb"
            # rezpdb=`getresol $file | awk '{print $2}' | awk -F'/' '{print $1}'`
            # check if its less than 3
            ##REZ=`echo $rezpdb '<=' 3.00 | bc -l`

            # if [ "$REZ" -eq "1" ]
            # then
            #     echo "$pdb_name has resolution of $REZ "
            #     echo -n " $pdb_name" >> $FILE_OUTPUT

        if [[ $torsion ]]
        then
            echo "torsion file name $TOR_OUTPUT"
            pdbtorsions $pdb_name_file > $torsion/${culled_pdb}_torsion.txt
        fi


            # fi
            
        # fi

    done
    # done

fi
echo "start code"

##########################################################################
#   carry out proline dataset extraction and machine learning
###########################################################################
echo "####################################################"
echo "####################################################"
for num in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
    /home/ayubh/project/git_clone/cis-proline-pred/scripts/./getpro_py.py -d $torsion $num > $CURRENT_DIRECTORY/temp.csv
    CurrentEncode=-"$ENCODER"
    cd "$CURRENT_DIRECTORY"
    echo "####################################################"
    pwd
    time /home/ayubh/project/git_clone/cis-proline-pred/scripts/./encoder.py $CurrentEncode $CURRENT_DIRECTORY/temp.csv $num > $CURRENT_DIRECTORY/temp_encoded.csv
    echo "encoder DONE!!!!!!!!! \n\n"
    cd "$CURRENT_DIRECTORY"
    echo "####################################################"
    pwd
    head -n 1 temp_encoded.csv | awk -F',' '{for(i=4;i<=NF;++i)print $i}' > inputs.txt
    echo "####################################################"
    echo "####################################################"
    echo "start machine learning"
    csv2arff -ni inputs.txt type temp_encoded.csv > temp.arff
    java $CLASSIFIER -d final_${ENCODER}_${num}.model -t temp.arff  > final_${ENCODER}_${num}.out

    echo "####################################################"
    echo "####################################################"
    echo "time to remove temp files"
    rm temp*


done



# for i in "${ourlsts[@]}"
# do 
#     echo "$i"
# done
   

#rezpdb=`getresol /home/ayubh/project/git_clone/cis-proline-pred/pdb/2wek.pdb | awk '{print $2}' | awk -F'/' '{print $1}'`