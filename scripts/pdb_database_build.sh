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




while getopts h:t:f:d:o:e:p:x:m:s: flag
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
        m) MACHINELEARNING=${OPTARG};;
        s) SECSTR=${OPTARG};;
        
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
            echo "chain extraction "
            cleaned_culled_pdb="${culled_pdb#pdb}"
            chain_name=`grep -i "${cleaned_culled_pdb}" cullpdb_pc25.0_res0.0-3.0_noBrks_noDsdr_len40-10000_R0.25_Xray_d2021_06_05_chains3940 | awk '{print $1}'`
            chain_letter=${chain_name#"${cleaned_culled_pdb^^}"}
            echo "chain letter is $chain_letter" 
            pdbgetchain $chain_letter $pdb_name_file > $torsion/${culled_pdb}_chain.ent

            echo "chain extracted to file $torsion/${culled_pdb}_chain.ent"
            pdbtorsions $torsion/${culled_pdb}_chain.ent > $torsion/${culled_pdb}_torsion.txt

            echo "doing a secondary structure extraction...."
            if [[ $SECSTR ]]
            then
                pdbsecstr $torsion/${culled_pdb}_chain.ent > $SECSTR/${culled_pdb}_sec.txt
                echo "$SECSTR/${culled_pdb}_sec.txt"

            echo "torsion extraction done and removing chain files"
            rm $torsion/${culled_pdb}_chain.ent

            echo "chain extraction done"
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
if [[ $MACHINELEARNING ]]
then
    for num in 9 10
    do
        /home/ayubh/project/git_clone/cis-proline-pred/scripts/./getpro_py.py -d $torsion -s $SECSTR -w $num > $CURRENT_DIRECTORY/temp.csv
        CurrentEncode=-"$ENCODER"
        cd "$CURRENT_DIRECTORY"
        echo "####################################################"
        pwd
        time /home/ayubh/project/git_clone/cis-proline-pred/scripts/./encoder.py $CurrentEncode $CURRENT_DIRECTORY/temp.csv $num > $CURRENT_DIRECTORY/temp_encoded.csv
        # create several csv files with equal amount cis and trans

        head -n 1 temp_encoded.csv > $CURRENT_DIRECTORY/temp_cis.csv
        grep "cis" $CURRENT_DIRECTORY/temp_encoded.csv >> $CURRENT_DIRECTORY/temp_cis.csv
        grep "trans" $CURRENT_DIRECTORY/temp_encoded.csv > $CURRENT_DIRECTORY/temp_trans.csv
        echo "encoder DONE!!!!!!!!! \n\n"
        cd "$CURRENT_DIRECTORY"
        /home/ayubh/project/git_clone/cis-proline-pred/scripts/./join_cis_trans.py $CURRENT_DIRECTORY/temp_cis.csv $CURRENT_DIRECTORY/temp_trans.csv 9
        echo "####################################################"
        pwd
        head -n 1 temp_encoded.csv | awk -F',' '{for(i=4;i<=NF;++i)print $i}' > inputs.txt
        echo "####################################################"
        echo "####################################################"
        echo "start machine learning model ${num}..........."
        
        for radfile in temp_rand*
        do
            rad_name=`basename $radfile .csv`
            echo "rad name $rad_name"
            csv2arff -ni inputs.txt type $radfile > $rad_name.arff
            java $CLASSIFIER -d ${rad_name}_${ENCODER}_${num}.model -t $rad_name.arff  > ${rad_name}_${ENCODER}_${num}.out

            echo "Machine learning finished"
            cat ${rad_name}_${ENCODER}_${num}.out | grep -A 20 Stratified | grep Weighted
            cat ${rad_name}_${ENCODER}_${num}.out | grep -A 20 Stratified | grep Weighted | awk 'BEGIN {sum=0; fold=0} {sum+=$8; fold++} END {print "Mean MCC: " sum/fold}'
        done
        echo "####################################################"
        echo "####################################################"
        echo "time to remove temp files"
        rm temp*
        rm inputs.txt

    done
fi

# for i in "${ourlsts[@]}"
# do 
#     echo "$i"
# done
   


#rezpdb=`getresol /home/ayubh/project/git_clone/cis-proline-pred/pdb/2wek.pdb | awk '{print $2}' | awk -F'/' '{print $1}'`