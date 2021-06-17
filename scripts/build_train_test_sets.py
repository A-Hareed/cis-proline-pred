#! /usr/bin/python3


# import libiries 
import sys
import random

#-----------------------------------------------------------
def read_file(filename):
    # dictionary to have pdb name plus atom number as keys
    file_dict = {}
    with open(filename, 'r') as f:
        file_list = f.read().splitlines()
    for line in file_list:
        temp_lst = line.split(',')
        key = temp_lst[0] + '_' + temp_lst[1]
        value = temp_lst[2:]

        # add line to dictionary
        file_dict[key] = value

    return (file_dict) #returns a dictionary


#-----------------------------------------------------------
def header_input(filename):
    with open(filename, 'r') as f:
        result = f.read()
    return (result)

def get_cisdataset(cis_dic, fold):
    """

    """
    
    keys = cis_dic.keys()
    pdb_lst = []
    for i in keys:
        split_point = i.rfind('_')
        pdbname = i[:split_point]
        pdb_lst.append(pdbname)
    distinct_pdblst = set(pdb_lst)
    amount_test = round((len(distinct_pdblst) * (fold/100)), 0)
    amount_train = len(distinct_pdblst) - amount_test
    # print(amount_test)
    # create cis_test cis_testing_set
    cis_test_pdbused = [] # used to keep used cis dataset to prevent duplications
                          # between test sets
    cis_test_lst = []
    avalible_pdb = list(distinct_pdblst)

    random.seed(43)
    r = random.SystemRandom()
    r.shuffle(avalible_pdb)
    
    for num in range(1,6):
        temp_lst = []
        # used to remove the used pdb
        if (len(cis_test_pdbused) > 0):
            for item in cis_test_pdbused:
                avalible_pdb.remove(item)
                
            cis_test_pdbused = []
        for i in range(int(amount_test)):
            
            if (i < len(avalible_pdb)):
                pdb = avalible_pdb[i]
                cis_test_pdbused.append(pdb)
                for k, v in cis_dic.items():

                    underscr = k.rfind('_')
                    key_prefix =  k[:underscr]
                    key_suffix = k[(underscr+1):]

                    if (key_prefix == pdb):
                        line = ''

                        for n,data in enumerate(v):
                            if (n == 0):
                                line += key_prefix + ',' + key_suffix + ',' + data

                            if ( n > 0 and   n < (len(v) -1)):
                                line +=  ',' + data
                                
                            elif (n == (len(v) - 1)):
                                line += ',' + data + '\n'
                                
                        temp_lst.append(line)

            # else:
                # print(f'{len(avalible_pdb)} {i}')
        cis_test_lst.append(temp_lst)
    
    # create test dataset 
    cis_training_lst = []
    
    for i in range(5):

        # remove one batch and combine the remaining four
        # test batches
        # print (i)
        temp_lst = []

        for k in cis_test_lst:
            if k != cis_test_lst[i]:
                temp_lst.extend(k)
        
        # print(len(temp_lst))
        cis_training_lst.append(temp_lst)
    # print(cis_training_lst)   
    set1 = set(cis_test_lst[0])
    set2 = set(cis_test_lst[1])
    c = set1.intersection(set2)

    # print(cis_test_lst[0][-1])
    # print(cis_test_lst[1][-1])
    # print(f'the union between 1 and 2 {len(c)}')

    return (cis_test_lst, cis_training_lst)

#-----------------------------------------------------------
def get_transdataset(trans_dic, num = 5):

    amount_test = int(round((len(trans_dic.keys())) / 5, 0))
    
    # create a list of keys to tehn randomly shuffle for selection test selection
    keys_lst = list(trans_dic.keys())
    
    random.seed(43)
    r = random.SystemRandom()
    r.shuffle(keys_lst)
    # print(len(keys_lst))

    # create testing trans dataset
    trans_test_lst = []
    trans_data_used = []
    
    for i in range(num):
        temp_lst = []

        if (len(trans_data_used) > 0):
            for item in trans_data_used:
                keys_lst.remove(item)
            trans_data_used = []

        for size in range(amount_test):
            line = ''
    
            if (size < len(keys_lst)):
                data_key = keys_lst[size]
                trans_data_used.append(keys_lst[size])

                data_value = trans_dic[data_key]

                underscr = data_key.rfind('_')
                key_prefix = data_key[:underscr]
                key_suffix = data_key[(underscr+1):]
                
                for n, data in enumerate(data_value):
                    if (n == 0):
                        line += key_prefix + ',' + key_suffix + ',' + data
                    
                    if ( n > 0 and   n < (len(data_value) - 1)):
                        line += ',' + data
                    elif (n == (len(data_value) - 1)):
                        line += ',' + data + '\n'
            
            temp_lst.append(line)
        trans_test_lst.append(temp_lst)
    
    # create the training batchs
    trans_training_lst = []
    for i in range(5):
        
        # remove one batch and combine the remaining four
        # test batches
        # print(i)
        temp_lst = []
        
        for j in range(5):
            if (i != j):
                temp_lst.extend(trans_test_lst[j])
            

            # temp_lst.remove(trans_test_lst[i])
            # if k != trans_test_lst[i]:
                # print(k)

        # print(len(temp_lst), 'temp_lst')
        trans_training_lst.append(temp_lst)
    # print(cis_training_lst)
    my_set1 = set(trans_test_lst[0])

    my_set2 = set(trans_test_lst[1])
    c = my_set1.intersection(my_set2)
    # print(len(trans_test_lst))
    # print('training')
    # print(f'the union between 1 and 2 {len(c)}')
    # print(trans_test_lst[0][-1])
    # print(trans_test_lst[1][-1])

    return (trans_test_lst, trans_training_lst)
#------------------------------------------------------------------
def combine_cis_trans(cis_lst, trans_lst, header, train=None):
    result = ''
    multi_cis = []
    random.seed(43)
    r = random.SystemRandom()

    if (train != None):
        cis_trans_lst = []

        r.shuffle(trans_lst)




        multi = int(train)
        for i in range(multi):
            multi_cis.extend(cis_lst)
        cis_trans_lst.extend(multi_cis)
        print(len(cis_trans_lst))
        for i in range(len(cis_trans_lst)):
            cis_trans_lst.append(trans_lst[i])
        print(len(cis_trans_lst))
        # cis_trans_lst.extend(trans_lst)


        
        r.shuffle(cis_trans_lst)
        result += header
        result += ' '.join(cis_trans_lst)

    else:
        cis_trans_lst = []
        cis_trans_lst.extend(cis_lst)
        cis_trans_lst.extend(trans_lst)

        r.shuffle(cis_trans_lst)
        result += header
        result += ' '.join(cis_trans_lst)
    
    return (result)



#------------------------------------------------------------------
#           main program
#-----------------------------------------------------------

# takes in cis and trans files from commandline 
cis_filename = sys.argv[1]

fold = int(sys.argv[3])

outputname = sys.argv[4]

header = sys.argv[5]
title = ''
title += header_input(header)

print(f'header is :{title}')

trans_filename = sys.argv[2]

# create dictionaries 
cis_dict = read_file(cis_filename)
trans_dict = read_file(trans_filename)
cis_testing_set, cis_training_set = get_cisdataset(cis_dict, fold)
trans_testing_set, trans_training_set = get_transdataset(trans_dict)



x = 5 + (4*18)
print(x)

y = int(round(27816/1437, 0))
print(y)
print(f'cis test list batch sizes {len(cis_testing_set)}:-----------')
for i, j in enumerate(cis_testing_set):
    print(f'test batch {i+1} size: {len(j)}')

print(f'cis training list batch sizes {len(cis_training_set)}:-----------')
for i, j in enumerate(cis_training_set):
    print(f'training batch {i+1} size: {len(j)}')

print(f'trans test list batch sizes {len(trans_testing_set)}:-----------')
for i, j in enumerate(trans_testing_set):
    print(f'test batch {i+1} size: {len(j)}')

print(f'trans training list batch sizes {len(trans_testing_set)}:-----------')
for i, j in enumerate(trans_training_set):
    print(f'training batch {i+1} size: {len(j)}')


# combine_cis_trans(cis_lst=cis_training_set[0], trans_lst=trans_training_set[0], header= title, train=9)



for i in range(5):
    out_file_test = outputname + '_test_' + str(i) + '.csv'
    out_file_training = outputname + '_train_' + str(i) + '.csv'

    combine_train = combine_cis_trans(cis_lst=cis_training_set[i], trans_lst= trans_training_set[i], header=title, train=4)
    combine_test = combine_cis_trans(cis_lst=cis_testing_set[i], trans_lst= trans_testing_set[i], header= title)


    with open(out_file_training, 'w') as f:
        f.write(combine_train)

    with open(out_file_test, 'w') as f:
        f.write(combine_test)



