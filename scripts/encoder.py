#!/usr/bin/python3
#*************************************************************************
#
#   Program:    encoder
#   File:       encoder.py
#
#   Version:    V1.0
#   Date:       18.05.21
#   Function:   Encodes residues in a csv file
#               given encoding type 
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
#   V1.0   18.05.21  Original   By: Ayub Hareed
#   V2.0   10.06.21             By: Ayub Hareed
#*************************************************************************

# import libraries 
import sys
import utilities
import string
import os 
#*************************************************************************
# function reads in the file
def read_csv_file(filename):
    with open(filename, 'r') as f:
        # read in the file and remove \n
        file_raw = f.read().splitlines()
        csv_file = []
        # splits line by comma
        for line in file_raw:
            if ('#' not in line):
                lst = line.split(',')
                csv_file.append(lst)
    return (csv_file)
#*************************************************************************
def csv_header(num, window, pro_lst):
    """
    input: num (intiger) - to show how many ### the encoder has
           window (intiger) - 
    returns: string that contains the encoder header 
    """
    # imports the alphabet to use it on the 
    # prefix of header
    letters = string.ascii_lowercase
    # since window equal sequnce size of either 
    # N-terminal or C-terminal


    window = window * 2
    result = ''
    
    # if another encoder is used ontop of the general encoders
    if (len(pro_lst) > 0):
        lst = pro_lst[2]  # get a line of the csv file
        
        encoded_sz = len(lst[3:])

        # the loop is used to make the header 
        for prefix in range(0,window):
            for suffix in range(1,(num + 1)):
                result += ',' + letters[prefix] + str(suffix)
        
        # append the second encoder to the csv header
        if (encoded_sz > window):
            result += ',sec1,sec2' 

    return (result)

#*************************************************************************
def amino_acid_encoder(proline_csv, encoder):
    """
    input: proline_csv (list of strings) - contains proline torsion csv output
    return: converts amino acid one letter code to encoder
    """
    result = '' # used to concatinate the csv columns 
    for line in proline_csv:
      
        # if statement ignores blank lines
        if len(line) > 1:

        # add the pdb name, atom number and torsion angle type
            result += line[0] + ',' + line[1] + ',' + line[2] + ','
            
            # encode one letter amino acid 
            if ('*' in line[-1]):
                sec_encode = utilities.Encode('../encoder_data/SecondaryStructure.txt', 'sec')
                sec_dict = sec_encode.get_encode_dict()
                line_test = line[-1].replace('*','')
                if line_test in sec_dict.keys():
                    for i, item in enumerate(line):
                        
                        # to insure that the line doesn't end with a comma
                        if (i > 2 and i < (len(line) - 1)):
                            if (item in encoder.keys()):  # checks if the correct amino acid is entered

                                encoded_amino_acid = encoder[item]
                                result += str(encoded_amino_acid) + ','

                        # last term
                        elif (i > 2 and i == (len(line) - 1)):
                            # checks if the correct amino acid is entered
                            item = item.replace('*', '')
                            sec_encode = utilities.Encode('../encoder_data/SecondaryStructure.txt', 'sec')
                            sec_dict = sec_encode.get_encode_dict()
                            if (item in sec_dict.keys()):
                                encoded_amino_acid = sec_dict[item]
                                result += str(encoded_amino_acid) + '\n'
                else:
                    no_sec = f'this secondary structure not found: {item}'
                    with open('/home/ayub/Desktop/cis_proline/pisces/test/cathe_encode.out', 'a') as f:
                        f.write(f'{no_sec}\n')
                    continue
 
            else:
                for i, item in enumerate(line):

                    # to insure that the line doesn't end with a comma
                    if (i > 2 and i < (len(line) - 1)):
                        if (item in encoder.keys()):  # checks if the correct amino acid is entered

                            encoded_amino_acid = encoder[item]
                            result += str(encoded_amino_acid) + ','
                    # last term
                    elif (i > 2 and i == (len(line) - 1)):
                        if (item in encoder.keys()):  # checks if the correct amino acid is entered
                            encoded_amino_acid = encoder[item]
                            result += str(encoded_amino_acid) + '\n'
    return (result)



# ------------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------------
window = 3
if(len(sys.argv) == 4):
    window = int(sys.argv[3])

# if ('-s' in sys.argv):
#     i = sys.argv.index('-s')
#     sec_encode = sys.argv[i]
# else:
#     sec = None

# using blosum45 as encoder
if(sys.argv[1] == '-b45'):
    blosum45 = utilities.Encode('../encoder_data/BLOSUM45', 'blosum45')
    encoder = blosum45.get_encode_dict()
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    header = csv_header(20, window, proline_csv)
    print('pbd,atom num,type{}'.format(header)) 
    print(amino_acid_encoder(proline_csv, encoder))

# using blosum62 as encoder
if(sys.argv[1] == '-b62'):
    blosum62 = utilities.Encode('../encoder_data/BLOSUM62', 'blosum62')
    encoder = blosum62.get_encode_dict()
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    header = csv_header(20, window, proline_csv)
    print('pbd,atom num,type{}'.format(header))
    print(amino_acid_encoder(proline_csv, encoder))

# using blosum80 as encoder
if(sys.argv[1] == '-b80'):
    blosum80 = utilities.Encode('../encoder_data/BLOSUM80', 'blosum80')
    encoder = blosum80.get_encode_dict()
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    header = csv_header(20, window, proline_csv)
    print('pbd,atom num,type{}'.format(header))
    print(amino_acid_encoder(proline_csv, encoder))

# using blosum90 as encoder
if(sys.argv[1] == '-b90'):
    blosum90 = utilities.Encode('../encoder_data/BLOSUM90', 'blosum90')
    encoder = blosum90.get_encode_dict()
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    header = csv_header(20, window, proline_csv)
    print('pbd,atom num,type{}'.format(header))
    print(amino_acid_encoder(proline_csv, encoder))


if(sys.argv[1] == '-t5'):
    tscale5 = utilities.Encode('../encoder_data/TScale5.txt', 'tscale5')
    encoder = tscale5.get_encode_dict()
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    header = csv_header(5, window, proline_csv)
    print('pbd,atom num,type{}'.format(header))
    print(amino_acid_encoder(proline_csv, encoder))


if(sys.argv[1] == '-a4'):
    abhinandan4 = utilities.Encode('../encoder_data/Abhinandan4.txt', 'abhinandan4') 
    encoder = abhinandan4.get_encode_dict()
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    header = csv_header(4, window, proline_csv)
    print('pbd,atom num,type{}'.format(header))
    print(amino_acid_encoder(proline_csv, encoder))

#*************************************************************************
#   first function handles argv arguments and error inputs from the 
#   command line along with the help (-h) input


#*************************************************************************

