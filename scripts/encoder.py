#!/usr/bin/python3
#*************************************************************************
#
#   Program:    encoder
#   File:       encoder.py
#
#   Version:    V1.0
#   Date:       18.05.21
#   Function:   Encodes residues in a csv file
#               using 
#
#   Author:     Ayub Hareed
#   
#   EMail:      ayubm56@gmail.com
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
#*************************************************************************

# import libraries 
import csv
import sys
import utilities


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
            for i, item in enumerate(line):

                if (i > 2 and i < (len(line) -1)):  # to insure that the line doesn't end with a comma
                    if (item in encoder.keys()): # checks if the correct amino acid is entered

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

# using blosum45 as encoder
if(sys.argv[1] == '-b45'):
    encoder = utilities.blosum45_dict
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    print(amino_acid_encoder(proline_csv, encoder))

# using blosum62 as encoder
if(sys.argv[1] == '-b62'):
    encoder = utilities.blosum62_dict
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    print(amino_acid_encoder(proline_csv, encoder))

# using blosum80 as encoder
if(sys.argv[1] == '-b80'):
    encoder = utilities.blosum80_dict
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    print(amino_acid_encoder(proline_csv, encoder))

# using blosum90 as encoder
if(sys.argv[1] == '-b90'):
    encoder = utilities.blosum90_dict
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    print(amino_acid_encoder(proline_csv, encoder))


if(sys.argv[1] == '-t5'):
    encoder = utilities.tscale5_dict
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    print(amino_acid_encoder(proline_csv, encoder))


if(sys.argv[1] == '-a4'):
    encoder = utilities.abhinandan4_dict
    proline_csv_file = sys.argv[2]
    proline_csv = read_csv_file(proline_csv_file)
    print(amino_acid_encoder(proline_csv, encoder))

#*************************************************************************
#   first function handles argv arguments and error inputs from the 
#   command line along with the help (-h) input

#*************************************************************************
