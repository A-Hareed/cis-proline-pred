#! /usr/bin/python3
#*************************************************************************
#
#   Program:    join_cis_trans
#   File:       join_cis_trans.csv
#
#   Version:    V1.0
#   Date:       26.05.21
#   Function:   splits encoded cis/trans proline dataset
#               into muliple csv with equal amount of cis and trans
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
#   V1.0   25.05.21  Original   By: Ayub Hareed
#*************************************************************************

# import librearies
import sys
import string
import random 
#********************************************************************
def read_in_csv(filename):
    """
    input filename (string) - takes in file name from the 
                              proline csv dataset  

    returns file_lst (list of strings) - returns a list of each 
                                         each individual line

    V1.0   25.05.21  Original   By: Ayub Hareed
    """

    # reads file in 
    with open(filename, 'r') as f:
        file_lst = f.read().splitlines() # splits csv file by line 
    return (file_lst)

#********************************************************************
def test_split(cis_file, trans_file, multiple):
    """
    input 


    """
    
    #  find how much of the file to split the file
    cis_length = len(cis_file[1:]) * multiple
    # print(cis_length)

    # random shuffle of trans data list
    random.seed(43)
    r = random.SystemRandom()
    r.shuffle(trans_file)

    # use the length to split the file
    file_num = []
    start = 0
    counter = 0
    initial_lst = []
    initial_lst.append(cis_file[0])

    # augmentation of cis file e.g copy several times to incease
    # cis dataset
    for num in range(0,multiple):
        initial_lst.extend(cis_file[1:])


    for line in trans_file:
        # print(counter)
        if (counter <= cis_length):
            initial_lst.append(line)
            counter += 1
        
        if (counter == cis_length):
            file_num.append(initial_lst)
            initial_lst = []
            initial_lst.extend(cis_file)
            counter = 0
    return (file_num)
#*********************************************************
def final_out(lst, num):
    """


    """
    file_lst = lst[num]
    result = ''
    for line in file_lst:
        result += line + '\n'
    return (result)

#*********************************************************
def file_suffix_name(num):
    """


    """
    
    letters = string.ascii_lowercase

    suffix_lst = []
    for suffix in range(0,num):
        suffix_lst.append(letters[suffix])
    return (suffix_lst)

#*********************************************************
def usage_die():
    """
    Prints a usage message and exits the program

    V1.0   25.05.21  Original   By: Ayub Hareed

    """
    print("""
join_cis_trans V1.0 Ayub Hareed

Usage: Using csv files that contain only encoded cis-proline data [file one]
       and encoded trans-proline data [file two], the two files are combined to create 
       multiple proline csv files with same cis-proline datasets but randomly shuffled
       trans datasets.
       encoded_cis_dataset.csv,  -- the encoded csv output from encoder.py  
       encoded_trans_dataset.csv    split using grep "cis" and grep "trans"
       
command example: ./join_cis_proline.py  [cis csv file] [trans csv file]

""")
    sys.exit()

#*********************************************************
#   main program
#*********************************************************

if (len(sys.argv) <= 2 or
    sys.argv[1] == '-h'):
    usage_die()

multiple = 1
if (len(sys.argv) > 3):
    multiple = int(sys.argv[3])

if (len(sys.argv) > 2):
    # read in the csv file that contains cis
    cis_filename = sys.argv[1]
    cis_list = read_in_csv(cis_filename)

    # read in the csv file that contains trans 
    trans_filename = sys.argv[2]
    trans_list = read_in_csv(trans_filename)




    num = len(test_split(cis_list,trans_list, multiple))
    print(num)
    out_file_lst = file_suffix_name(num)
    print(out_file_lst)
    # print(trans_list)

    # print(file_list[0][0])

    for i,a in enumerate(out_file_lst):
        out_file_name = 'temp_rand_1_' + a + '.csv'
        file_lst = test_split(cis_list,trans_list, multiple)
        file = final_out(file_lst,i)
        sys.stdout = open(out_file_name, 'w')
        print(file)
        sys.stdout.close()

