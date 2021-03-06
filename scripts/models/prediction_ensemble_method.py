#!/usr/bin/python3
#*************************************************************************
#
#   Program:    ensemble_prediction
#   File:       prediction_ensemble_method.py
#
#   Version:    V1.0
#   Date:       03.07.21
#   Function:   takes cis/trans prediction outputs from XGBoost (PROGRAM: boost.py) and
#               Random Forests (PROGRAM: weka) to produce a combined final preditction
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
#   Usage: cis/trans proline prediction from two machine learning classifiers.
#          commandline Example: ./boost.py [probalility threshold] -x [xgboost prediction file] -r [Random Forest prediction file]
#          ***the last parameter should be Random forest
#   ======
#
#*************************************************************************

# Import libraries
import sys
import math
import random

#------------------------------------------
def read_file(filename):
    """
    read in the proline predictions from Random Forest classifiers


    Input:   (string) filename - a filename for the txt file
    Returns: (list) lst - a list that each item corresponds to each line 
             of the prediction text file; e.g. [['1','cis','cis','0.70'],...] 
             where the second item is the actual label and the third item is the prediction

    03.07.21 Original By: Ayub Hareed
    """
    lst = []

    # read text file
    with open(filename, 'r') as f:
        file_lst = f.read().splitlines() # turn each line into list items
    counter = 0 # used to show skip the first line 
    for line in file_lst:
        if ('inst#' in line):
            counter += 1
            continue
        if (line == ''): # prevents adding empty lines 
            continue
    
        if (counter == 1):
            lst_line = line.split() # split each line into a list 
            lst.append(lst_line) # creates a list of lists 
    return (lst)

#------------------------------------------------------------
def read_xgb_file(filename):
    """
    read in the proline predictions from XGBoost classifiers


    Input:   (string) filename - a filename for the txt file
    Returns: (list) lst - a list that each item corresponds to each line
             of the prediction text file; e.g. [['1','cis','0.70'],...]

    03.07.21 Original By: Ayub Hareed
    """

    lst = []
    # read the xgboost prediction csv file 
    with open(filename, 'r') as f:
        file_lst = f.read().splitlines()
    # split using comma
    for line in file_lst:
        lst_line = line.split(',')
        lst.append(lst_line)

    
    # create a dictionary that has sample number as key
    # and type (cis/trans) and probability
    xgb_dict = {}
    count = 1
    for line in lst:
        xgb_dict[line[0]] = [line[1], float(line[2])]
        count += 1
    return (xgb_dict)
#------------------------------------------------------------
def calculate_mcc(tp,tn,fp,fn):
    """
    calculates the mcc score for a given predition


    Input:   (integers) tp,tn,fp,fn - ingers from actual lables and 
             predicted labels
    Returns: (float) mcc - mcc score

    03.07.21 Original By: Ayub Hareed
    """

    numerator = tp * tn - fp * fn
    denominator = (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)
    denominator_root = math.sqrt(denominator)
    if (denominator_root != 0):
        return (numerator / denominator_root)
    else:
        denominator_root = 1
        return (numerator / denominator_root)

#------------------------------------------
def vote_count(all_lst,p_input):
    """
    takes one or more Random Forest weka prediction outputs 
    and takes a pooled vote from each prediction.
    NOTE that each vote is weighted by its probability.


    Input:   (dictionary) all_lst - a dictionary containing all predictions
             (float) p_input - a float that is used for prediction probability 
                               threshold 

    Returns: (dictionary) majority_vote - a list that each item corresponds to each line
                                          of the prediction text file; e.g. [['1','cis','0.70'],...]
             (set) full_lst - a set that contains the numbers correponding to each 
                              testing sample

    03.07.21 Original By: Ayub Hareed
    """


    vote_dict = {}    # dictionary that would contain  testing dataset number as 
                      # the key and each vote and probability as the items

    majority_vote = {}  # a dictionary that contains the testing dataset number as
                        # the key and the class with the most votes as the items

    full_lst = set()    # contains the testing dataset number 

    # loops through a list that contains all the weka predictions
    # where each item is another list that corresponds to individual predictions
    for lst in all_lst:
        for line in lst:
            class_pred = line[2][2:]
            num = line[0]
            
            prob = float(line[-1])
            full_lst.add(num)
######################################################################        
            # probability threshold to cut off what predictions are added    
            if (prob >= p_input):
                if num not in vote_dict.keys():
                    vote_dict[num] = [[class_pred,prob]]
                else:
                    vote_dict[num].append([class_pred,prob])


    # if the all_lst has at least one prediction
    if len(all_lst) >= 1:
        for k, v in vote_dict.items():
            trans_score = float(0)  # a varible used to store the sum of all 
                                    # the trans probability for each prediction
                                    # sample.

            cis_score = float(0)    # a varible used to store the sum of all 
                                    # the cis probability for each prediction
                                    # sample.

            cis_count = float(0)    # stores the number of cis predicted for each
                                    # sample 

            trans_count = float(0)  # stores the number of cis predicted for each
                                    # sample
            
            # checks if at least one class is present                                     
            if ('cis' in v[0][0] or 'trans' in v[0][0]):
                # the item "v" contains multiple predictions and so loops through 
                # it. This is due to Random Forest having 20 predictions in this
                # project 
                for i in v:
                    
                    if (i[0] == 'cis'): 
                        cis_score += i[1]
                        cis_count += 1
                    if (i[0] == 'trans'):
                        trans_score += i[1]
                        trans_count += 1
                    if (trans_score > cis_score): 
                        trans_prob = trans_score/trans_count
                        majority_vote[k] = ['trans',trans_score, trans_prob]
                    if (trans_score < cis_score ):
                        cis_prob = cis_score/cis_count
                        majority_vote[k] = ['cis', cis_score, cis_prob]
                    
                    # If the score for cis and trans are equal 
                    # than a random choice is used to randomly select
                    # a class.
                    if (trans_score == cis_score): 
                        class_lst = ['cis', 'trans']
                        ran = random.choice(class_lst)
                        
                        if ran == 'cis':
                            majority_vote[k] = ['cis', cis_score]
                        if (ran == 'trans'):
                            majority_vote[k] = ['trans', trans_score]


    else: # if the list is empty than a notification is printed
        print('Random Forest predictions are empty!!!')
    return (majority_vote,full_lst)

#------------------------------------------
def counter(vote_dict, i):
    """
    takes a dictionary that contains XGBoost prediction and Random
    Forest predictions to give a final combinded prediction 
    NOTE that each vote from XGBoost and Rnadom Forest is weighted 
    by their probabilities.
    ***used in the function preformance***


    Input:   (dictionary) vote_dict - a dictionary that contains Random Forest
                                      and XGBoost prediction

             (integers) i - an integer that corresponds to the test sample number

    Returns: (dictionary) final - a dictionary that contains the final combined prediction

    03.07.21 Original By: Ayub Hareed
    """

    trans_count = 0
    cis_count = 0
    cis_score = 0 # 
    trans_score = 0
    final = {}
    
    for k, v in vote_dict.items():
        if v[0] == 'trans':
            trans_count +=1
            trans_score += float(v[1])
        elif v[0] == 'cis':
            cis_count +=1 
            cis_score += float(v[1])
    if trans_count > cis_count:
        final[i] = ['trans',1]
        return (final)
    elif cis_count > trans_count:
        final[i] = ['cis',1]
    elif cis_count == trans_count:
        print(f'\n\n######################\nprobsssssss\n{cis_score}\n{trans_score}\n\n\n')
        if cis_score > trans_score:
            final[i] = ['cis', 1]
        if (trans_score > cis_score):
            final[i] = ['trans', 1]
        # there is a chance that the two probs could be equal!!!

    return (final)

#------------------------------------------
def all_jury(RanF_dict, xgb_dict, st1):
    """
    takes dictionaries that contains XGBoost prediction and Random
    Forest predictions to give a final combinded prediction

    Input:   (dictionary) RanF_dict - a dictionary that contains Random Forest
                                      prediction
             (dictionary) xgb_dict - a dictionary that contains XGBoost prediction

             (list) st1 - a list that corresponds to the test sample numbers

    Returns: (dictionary) final - a dictionary that contains the final combined prediction

    03.07.21 Original By: Ayub Hareed
    """

    final_vote = {}
    # 1: cis, total, prob}
    print(f'############################################################\n############################\n###########\n{len(RanF_dict.keys())}############################################################\n############################\n###########\n')

    # loop through the testing samples individual number [determined by order]
    for i in st1:
        # if a prediction is found in both Random Forest and XGBoost
        if (i in RanF_dict.keys() and i in xgb_dict.keys()):
            vote = {'RanF': [RanF_dict[i][0],RanF_dict[i][2]], 'xgb': [xgb_dict[i][0],xgb_dict[i][1]]}
            result = counter(vote,i)
        # if a prediction is only given by XGBoost and not Random Forest (since it might not meet threshold)
        elif (i not in RanF_dict.keys() and i in xgb_dict.keys()):
            vote = {'RanF': 'unknown', 'xgb': [xgb_dict[i][0],xgb_dict[i][1]]}
            result = counter(vote,i)
        # add the combined vote to the  dictionary
        final_vote[i] = result[i]

    return (final_vote)
#------------------------------------------
def preformance(lst, vote_dict):
    """
    takes dictionaries that contains XGBoost prediction and Random
    Forest predictions to give a final combinded prediction

    Input:   (dictionary) vote_dict - a dictionary that contains cis/trans
                                      predictions

             (list) st1 - a list that actual sample classes (labels)
             
    Returns: (string) result - contains mcc results and predictions accuracy for
                               the given prediction

    03.07.21 Original By: Ayub Hareed
    """

    cis_correct = 0 # varible to store the correct cis number 
    cis_total = 0
    trans_correct = 0  # varible to store the correct trans number
    trans_total = 0
    
    # loops through actual sample labels.
    for line in lst:
        
        if line[0] in vote_dict.keys():
            if line[1][2:] == 'cis':

                guess = vote_dict[line[0]][0]
                if guess == 'cis':
                    cis_correct += 1
                cis_total += 1
            if line[1][2:] == 'trans':
                guess = vote_dict[line[0]][0]
                if guess == 'trans':
                    trans_correct += 1
                trans_total += 1




    if cis_total > 0:
        cis_accuracy = cis_correct/cis_total
    else:
        cis_accuracy = 0
    
    if trans_total > 0:
        trans_accuracy = trans_correct/trans_total
    else: 
        trans_accuracy = 0
    cis_wrong = cis_total - cis_correct
    trans_wrong = trans_total-trans_correct
    average = (cis_accuracy + trans_accuracy)/2
    # calculate mcc number
    cis_mcc = calculate_mcc(cis_correct,trans_correct,trans_wrong,cis_wrong)
    result = f'cis accuracy: {cis_accuracy}\ntrans_accuracy: {trans_accuracy}\navrg: {average}\ncis correct num: {cis_correct}\ncis wrong: {cis_total - cis_correct}\ntrans correct: {trans_correct}\ntrans wrong: {trans_total-trans_correct}\nMCC: {cis_mcc}\n{cis_correct+trans_correct+trans_wrong+cis_wrong}'

    return (result)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#       main program
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# get probability threshold from commandline or assigns one
if ('-w' != sys.argv[1]):
    prob_threshold = float(sys.argv[1])
    if (prob_threshold > 1):
        num = float(prob_threshold/100)
    else: 
        num = prob_threshold
else:
    num = 0.65

# Weka's Random Forest predictions 
predict_line = [] # a list to have all the Random Forest predictions

if ('-r' in sys.argv):
    i = sys.argv.index('-r')
    r = int(sys.argv[i+1])

print(f'the input len is: {len(sys.argv[r:])}')
# gets all the Random Forest prediction files
for i in sys.argv[r:]:
    filename = i
    print(filename)
    predict_line.append(read_file(filename))

vote_dict, full_lst = vote_count(predict_line, num)
# mcc for the weka models
print('just weka')
print(preformance(predict_line[0], vote_dict))


# XGBoost predictions 
if ('-x' in sys.argv):
    i = sys.argv.index('-x')
    x = int(sys.argv[i+1])
    xgb_dict = read_xgb_file(sys.argv[x])


print('#####################################################################################################################################')
# combined vote from both XGBoost and Random FOrest

lst = []
lst.extend(list(vote_dict.keys()))
lst.extend(list(xgb_dict.keys()))
st1 = set(lst)
final_vote = all_jury(vote_dict,xgb_dict, full_lst) # combined vote



if ('-x' in sys.argv and '-r' in sys.argv):
    print('both weka and xgboost')
    print(preformance(predict_line[0],final_vote))
