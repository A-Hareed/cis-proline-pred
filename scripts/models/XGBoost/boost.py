#! /usr/bin/python3
#*************************************************************************
#
#   Program:    boost
#   File:       boost.py
#
#   Version:    V1.0
#   Date:       20.06.21
#   Function:   build and test XGBoost models using cis/trans proline 
#               datasets
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
#   Usage: used to buid XGBoost models on cis/trans proline dataset
#   ======
#
#*************************************************************************

# Import libraries
import math
import xgboost as xgb
import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler  # normalise the dataset for machine learning

from sklearn.metrics import confusion_matrix # using sci kit learn model to extract tp, tn, fp, fn




#-------------------------------------------------------------
def readfile(filename):
    """
    read in the proline csv file and converts it into pandas dataframe


    Input:   (string) filename - a filename for the csv filr
    Returns: (DataFrame) df - a pandas dataframe where the first line 
             of the CSV file is the header

    20.06.21 Original By: Ayub Hareed
    """
    df = pd.read_csv(filename)
    return (df)
#-------------------------------------------------------------
def normalise(df):
    """
    data in panda dataframe is normalise using sklearn by removing the 
    mean and scaling to unit variance


    Input:   (DataFrame) df - a filename for the csv filr
    Returns: (DataFrames) - two dataframe where the label for the
             binary class is place in one DataFrame and the other 
             contains scaled features 

    20.06.21 Original By: Ayub Hareed
    """

    print(df.head())
    # df2 = df.drop(['pdb','atom num'], axis='columns')
    # df3 = df2.drop('atom num', axis='columns')

    #extract the features by dropping 'type' column
    x = df.drop('type', axis='columns')
    header = x.columns # removes the header
    # extract the label column 
    y = df[['type']]
    print(y.head())
    
    # convert the numinol label data into binary class 
    y['type'][y.type == 'trans'] = int(0)
    y['type'][y.type == 'cis'] = int(1)
    
    ## scale the features 
    scaler = StandardScaler()
    scaled_x = scaler.fit_transform(x)
  
    print(y.head())
    print(y.value_counts())
    df_scaled_x = pd.DataFrame(scaled_x, columns=header)
    
    return (df_scaled_x, y)



#-------------------------------------------------------------
def mcc_cal(y_actual, predictions):
    """
    calculates MCC

    Input:   (list) y_actual, predictions - the actual label and predictied label
    Returns: (float) mcc - MCC score

    20.06.21 Original By: Ayub Hareed    
    """

    # convert to intiger from string    
    y_actual['type'] = y_actual['type'].astype(str).astype(int)

    # extract true postive, true negative , false postive and false negative
    tn, fp, fn, tp = confusion_matrix(y_actual, predictions).ravel()

    # calcualte mcc 
    dinominator = (tp * tn) - (fp*fn)
    numirator = (tp + fp) * (tp + fn) * (tn+fp) * (tn+fn)
    root_numirator = math.sqrt(numirator)
    mcc = dinominator/root_numirator

    return (mcc)
#-------------------------------------------------------------
def model_build(x,y, weight, max_del):
    """
    takes in the training set and trains an XGBoost model


    Input:   (DataFrame) x,y - the training features and label
             (float) weight, max_del - XGBoost parameters

    Returns: (XGBoost model) model - using the x and y input an 
             XGBoost model is built

    20.06.21 Original By: Ayub Hareed    
    """

    # convert to intiger from string
    y['type'] = y['type'].astype(str).astype(int)

    # the model xgboost requires to first run DMatrix for x and y
    dtrain = xgb.DMatrix(x, label=y)


    # dictonary containing the parameters used for building XGBoost
    # the  num_parallel_tree and sample parameters are used to create 
    # a Random Forest like model of XGBoost
    tree_param = {'max_depth': 5, 'eta': 0.1, 'num_parallel_tree': 100, 'scale_pos_weight': weight, 'max_delta_step': max_del,
              'colsample_bynode': 0.8, 'subsample': 0.8,  'objective': 'binary:logistic', 'tree_method': 'exact'}

    # trainning the model 
    bst = xgb.train(tree_param, dtrain, 20)

    return (bst)

#-------------------------------------------------------------
def model_pred(model,x_test):
    """
    takes in the testing set and to get XGBoost preditictions 


    Input:  (1) (DataFrame) x_test - the test features 
            (2) (XGBoost model) model - using the x and y input an 
                XGBoost model is built
    Returns: predtions from the model

    20.06.21 Original By: Ayub Hareed    
    """

    dtest = xgb.DMatrix(x_test)
    ypred = model.predict(dtest)

    return (ypred)
#-------------------------------------------------------------
def save_pred(y_actual, ypred):
    """
    creates a string that contains all the predictions from 
    the XGBoost model


    Input:   (lisy) y_actual, ypred - the training features and label
             (float) weight, max_del - XGBoost parameters

    Returns: (string) final_result - a string that contains all the 
                      predictions from the XGBoost model

    20.06.21 Original By: Ayub Hareed    
    """

    # convert the y_test DataFrame to a list
    y_test_lst = y_actual['type'].tolist()

    y_act = []
    y_pred = []
    prediction = []
    cis = 0
    trans = 0
    final_result = ''
    # get each prediction in a line with data number, predition class and their probalility
    for i, prob in enumerate(ypred):

        if (prob <= 0.50 or prob >= 0.50):
            if (prob > 0.5):
                # print('cis', prob[0])
                y_pred.append(1)
                y_item = y_test_lst[i]
                y_act.append(y_item)
                final_result += str(i+1) + ',cis,' + str(prob) + '\n'

        if (prob < 0.5):
            # print('trans', prob[1])
            y_pred.append(0)
            y_item = y_test_lst[i]
            y_act.append(y_item)
            trans_prob = 1 - prob
            final_result += str(i+1) + ',trans,' + str(trans_prob) + '\n'
    
    return (final_result)


#-------------------------------------------------------------
#       main program
#-------------------------------------------------------------

# read in the trainning and the testing dataset
if '-f' in sys.argv:
    i = sys.argv.index('-f')
    f = int(sys.argv[i+1])
    filename = sys.argv[f]
    df = readfile(filename)

if '-t' in sys.argv:
    i = sys.argv.index('-t')
    t = int(sys.argv[i+1])
    df_test = readfile(sys.argv[t])


# read in weight and max_delta
if '-w' in sys.argv:
    i = sys.argv.index('-w')
    w = int(sys.argv[i+1])
    weight = float(sys.argv[w])
else:
    weight = 25.0

if '-m' in sys.argv:
    i = sys.argv.index('-m')
    m = int(sys.argv[i+1])
    max_del = float(sys.argv[m])
else:
    max_del = 1.0

# location to save the xgboost prediction
if '-l' in sys.argv:
    i = sys.argv.index('-l')
    l = int(sys.argv[i+1])
    file_location = sys.argv[l]



# normailise the datasets and split the features and 
# class labels  
x, y = normalise(df)
x_test, y_actual = normalise(df_test)

# build model

model = model_build(x, y, weight, max_del)

# test model
ypred = model_pred(model, x_test)

predictions = [round(value) for value in ypred]
mcc = mcc_cal(y_actual, predictions)

print(f'mcc:{mcc}')

if 'file_location' in globals():
    file_location_name = file_location + f'/result_xgb_pred.csv'
    # get predictions
    final_result = save_pred(y_actual, ypred)
    with open(file_location, 'w') as f:
        f.write(final_result)

#---------------------------------------------------------------------------------
