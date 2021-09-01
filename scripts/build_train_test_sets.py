#! /usr/bin/python3
#*************************************************************************
#
#   Program:    build_train_test_sets
#   File:       build_train_test_sets.py
#
#   Version:    V1.0
#   Date:       01.06.21
#   Function:   takes proline datasets and splits it into training and testing sets by
#               outputing undersampled training set for Random Forest and imbalanced 
#               training set for XGBoost 
#               
#
#   Author:     Ayub Hareed
#
#
#   EMail:     ayubm56@gmail.com
#
#*************************************************************************
#
#   This program is not in the public domain, but it may be copied
#   according to the conditions laid out in the accompanying file
#   COPYING.DOC
#
#   The code may be modified as required, but any modifications must be
#   documented so that the person responsible can be identified. If
#   someone else breaks this code, I don't want to be blamed for code
#   that does not work!
#
#   The code may not be sold commercially or included as part of a
#   commercial product except as described in the file COPYING.DOC.
#
#*************************************************************************
#
#   Usage: used to split proline dataset into training and testing samples
#
#   commandline Example: ./build_train_test_sets.py [proline csv file] [location to save file]
#   ======
#
#*************************************************************************


# Import libraries
import sys
import random
import pandas as pd


#------------------------------------------------------------------------------------------------------------------------------------------------------
def read_file(filename):
    """
    read in the proline csv file and converts it into pandas dataframe


    Input:   (string) filename - a filename for the csv proline file
    Returns: (DataFrame) df - a pandas dataframe where the first line
             of the CSV file is the header

    01.06.21 Original By: Ayub Hareed
    """
    df = pd.read_csv(filename)
    return (df)
#------------------------------------------------------------------------------------------------------------------------------------------------------
def get_train_test(df1, used_cis):
    """
    using pandas and a list that contains cis proline usage  
    to split into training and testing set


    Input:   (DataFrame) df1 - a pandas dataframe that consits of proline 
                               dataset

             (list) used_cis - a list that contains cis proline used to in 
                               test sets 

    Returns: (DataFrame) df_train - a pandas dataframe that contains training
                                    datasets

             (DataFrame) df_test - a pandas dataframe  that contains training
                                   datasets

    01.06.21 Original By: Ayub Hareed
    """

    # remove non-feature and label columns
    df = df1.drop(['pdb', 'atom num'], axis='columns')
    cis = df[df['type'] == 'cis'] # asign cis samples to new variable 

    # find the amount of cis to split inot five sets
    cis_num = cis.type.value_counts()
    num = int(int(cis_num[0])/5)
    
    print(f'\n\n#########################\ncis test length = {num}\n\n')
    uncut_cis_full = cis.drop(used_cis)  # drop the used cis samples to avoid 
                                         # cross-contamination

    cis_test = uncut_cis_full.sample(num)  # randomly select "num" amount of cis

    ct_index = cis_test.index.values.tolist()

    cis_train = cis.drop(ct_index)  # drop the selected training cis


    used_cis.extend(ct_index) # update the cis used list

    # now do the trans dataset

    trans = df[df['type'] == 'trans']

    trans_test = trans.sample(num)  # randomly select "num" amount of trans
    
    tt_index = trans_test.index.values.tolist()

    trans_train = trans.drop(tt_index)  # drop the selected training trans

    # combine trans and cis dataframes
    df_train = pd.concat([trans_train, cis_train], axis=0) 
    
    df_test = pd.concat([trans_test, cis_test], axis=0)

    return (df_train, df_test, used_cis)

#-------------------------------------------------------------------------------------------------------------------------------------------------------
def training_set(df):
    """
    using training dataframe the trans samples are undersampled 
    to use for Random Forest


    Input:   (DataFrame) df - a pandas dataframe that consists of proline 
                              training dataset


    Returns: (DataFrame) df_final - a pandas dataframe that consits of cis
                                    proline samples and undersampled trans
                                    samples

    01.06.21 Original By: Ayub Hareed
    """

    cis = df[df['type'] == 'cis']
    trans = df[df['type'] == 'trans']
    cis_num = cis.type.value_counts()
    # gets number of cis samples 
    sample_size = int(cis_num[0])
    
    trans_training_set = trans.sample(sample_size)  # randomly samples trans using 
                                                    # cis sample size

    # combine trans and cis samples to one dataframe                                                    
    df_final = pd.concat([trans_training_set, cis], axis=0)

    return (df_final)

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#           main program
#-------------------------------------------------------------------------------------------------------------------------------------------------------

# get proline dataset filename
filename = sys.argv[1]

# get location to save training and testing files
if (len(sys.argv) > 2):
    file_location = sys.argv[2]
else:
    file_location = ''


used_cis = []
df = read_file(filename)
df1 = df.dropna() # drop any rows with missing values


for i in range(1, 6):
    df_train, df_test, used_cis = get_train_test(df1, used_cis)

    # export testing samples
    test_location = file_location + '/test_' + str(i) + '.csv'
    df_test.to_csv(f'{test_location}', index=False)
    print(f'amount of cis used {len(used_cis)}')

    # weka Random Forest 20 undersampled training sets
    for t_num in range(1, 21):
        df_final = training_set(df_train)
        train_location = file_location + '/train_c' + str(i) + '_t' + str(t_num) + '.csv'
        df_final.to_csv(f'{train_location}', index=False)

        if t_num == 20:
            print(df_final.type.value_counts())
    
    # XGBoost training sets
    train_location = file_location + '/xg_train_c' + str(i) + '.csv'
    df_train.to_csv(f'{train_location}', index=False)

