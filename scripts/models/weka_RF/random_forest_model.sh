#! /usr/bin/bash
#*************************************************************************
#
#   Program:    random_forest
#   File:       random_forest_model.sh
#
#   Version:    V1.0
#   Date:       18.05.21
#   Function:   build and test Random Forest models using weka on
#               proline datasets
#*************************************************************************

# set up weka first 
# export WEKA=/nas/backup/work/newserver/bsmhome/zcbthhn/weka-3-8-3
# export WEKA=/home/ayub/Downloads/weka-3-8-5-azul-zulu-linux/weka-3-8-5
# Insert weka path:
export WEKA=

export CLASSPATH="$WEKA/weka.jar"
CLASSIFIER="weka.classifiers.trees.RandomForest"


# get the feature headers from csv files inoder to make arff files
head -n 1 test_1.csv | awk -F',' '{for(i=2;i<=NF;++i)print $i}' > input.txt


# loop through the five sets of test files along with each of its 
# corresponding 20 training sets
for num in $(seq 1 5)
do
    file_num=`echo test_${num}.csv`
    echo "${file_num}" 
    wc -l ${file_num}
    test_name=`basename ${file_num} .csv`
    training_letter=`echo c${num}`
    echo "${training_letter}"
    train=`echo train_c${num}`
    echo "${train}"
    echo "${train}" >> mcc_output.txt

    # extract testing arff file
    csv2arff -ni input.txt type ${file_num} >${test_name}.arff

    # loop through training sets
    for file in $train*.csv
    do
        wc -l ${file}
        filename=`basename ${file} .csv`
        # do csv extract
        
        csv2arff -ni input.txt type $file >$filename.arff
        echo "building model: ${filename} ***********"
        
        java $CLASSIFIER -I 500 -t $filename.arff -d RF500_${filename}.model > RF500_${filename}.out
        java $CLASSIFIER -T ${test_name}.arff -p 0 -l RF500_${filename}.model >predicted_with_RF500_${filename}.out
	    echo "filename = ${filename}"

    done 

done

# rm -f input.txt