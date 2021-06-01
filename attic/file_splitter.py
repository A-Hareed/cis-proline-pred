#! /usr/bin/python3

# import librearies
import sys
import string

#*********************************************************
def read_in_csv(filename):
    with open(filename, 'r') as f:
        file_lst = f.read().splitlines()
    return (file_lst)

#*********************************************************
def split_file(file_list, amount):
    amount = amount/100
    #  find how much of the file to split the file
    file_length = round((len(file_list) * amount), 0)

    # use the length to split the file 
    file_num = []
    lines = int(file_length) 
    start = 0
    end = lines
    while end <= len(file_list):
        file_1 = ''
        if (start == 0):
            file_num.append(file_list[:end])
            # print('start: {}  end: {}  length: {}'.format(start, end, len(file_list)))
            start = lines

        if (start > 0 and end < len(file_list)):
            end += lines
            file_line = [file_list[0]] + file_list[start:end]
            file_num.append(file_line)
            # print('start: {}  end: {}'.format(start,end))
            start += lines
        

    return (file_num)

#*********************************************************
def final_out(lst, num):
    file_lst = lst[num]
    result = ''
    for line in file_lst:
        result += line + '\n'
    return (result)

#*********************************************************
def file_suffix_name(num):
    
    letters = string.ascii_lowercase

    suffix_lst = []
    for suffix in range(0,num):
        suffix_lst.append(letters[suffix])
    return (suffix_lst)

#*********************************************************
#   main program
#*********************************************************

amount = 50

if len(sys.argv) > 2:
    amount = int(sys.argv[2])
if amount > 100:
    amount = 100

filename = sys.argv[1]
file_list = read_in_csv(filename)
#print(split_file(file_list,amount))
num = len(split_file(file_list, amount))
out_file_lst = file_suffix_name(num)
print(out_file_lst)

# print(file_list[0][0])

for i,a in enumerate(out_file_lst):
    out_file_name = 'temp_' + a + '.csv'
    file_lst = split_file(file_list, amount)
    file = final_out(file_lst,i)
    sys.stdout = open(out_file_name, 'w')
    print(file)
    sys.stdout.close()

