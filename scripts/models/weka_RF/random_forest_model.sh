#! /usr/bin/bash

echo "start!!!"


while getopts h:e: flag
do
    case "${flag}" in
            h) help_input="RUN";;
            e) encoder=${OPTARG};;

          [?]) printf >&2 "###############################################"
    esac
done

# export WEKA=/nas/backup/work/newserver/bsmhome/zcbthhn/weka-3-8-3
export WEKA=/home/ayub/Downloads/weka-3-8-5-azul-zulu-linux/weka-3-8-5
export CLASSPATH="$WEKA/weka.jar"
CLASSIFIER="weka.classifiers.trees.RandomForest"

# head -n 1 ${encoder}_test_1.csv | awk -F',' '{for(i=2;i<=NF;++i)print $i}' > input.txt

for num in $(seq 1 5)
do
    file_num=`echo ${encoder}_test_${num}.csv`
    echo "${file_num}" 
    wc -l ${file_num}
    test_name=`basename ${file_num} .csv`
    training_letter=`echo c${num}`
    echo "${training_letter}"
    train=`echo ${encoder}_train_c${num}`
    echo "${train}"
    echo "${train}" >> mcc_output.txt
    # extract testing arff file
    csv2arff -ni input.txt type ${file_num} >${test_name}.arff

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