#! /usr/bin/python3

# @data

# import libriries
import sys


#******************************************************
def read_csv_file(filenames):
    file_lst = []
    for filename in filenames:
        with open(filename, 'r') as f:
            file = f.readlines()
            file_lst.append(file)
    return (file_lst)



#******************************************************
def concat_file(lst):
    file = ''
    counter = 0
    if counter == 0:
        for line in lst[0]:
            file += line
        counter = 1
    if counter == 1:
        for cat in lst[1:]:
            match = 0
            for line in cat:
                if match ==1:
                    file += line

                if line == '@data\n':
                    match = 1
    return (file)





filename = sys.argv[1:]
file_lst = read_csv_file(filename)
print(concat_file(file_lst))

