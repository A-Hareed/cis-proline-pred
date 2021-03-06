#!/usr/bin/python3
#*************************************************************************
#
#   Program:    utilities
#   File:       utilities.py
#
#   Version:    V1.0
#   Date:       18.05.21
#   Function:   houses general variable, dictionaries and functions used by
#               needed to run other programs
#
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
#       programs that uses this file:
#           1. getpro_py
#           2. encoder.py
#*************************************************************************
#
#   Revision History:
#   =================
#   V1.0   01.05.21  Original   By: Ayub Hareed
#   V2.0   10.06.21             By: Ayub Hareed
#*************************************************************************
# import libraries 
import os


# import config

# file path configuration
file_path = os.path.realpath(__file__)
#print(file_path)
dir_path = os.path.dirname(file_path)
os.chdir(dir_path)

#*************************************************************************
# protein one letter code look up table
prot_seq = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N','ASP': 'D', 'CYS': 'C',
            'GLU': 'E', 'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
            'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
            'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
            'OBN': 'F', '2MR': 'R', 'ABA': 'A', 'ALY': 'K', 'AME': 'M',
            'AYA': 'A', 'BFD': 'D', 'BLE': 'L', 'CAF': 'C', 'CAS': 'C',
            'CME': 'C', 'CSD': 'C', 'CSO': 'C', 'CSP': 'C', 'CSX': 'C',
            'CXM': 'M', 'FF9': 'K', 'FME': 'M', 'GFT': 'S', 'HIC': 'H',
            'HSK': 'H', 'KCX': 'K', 'KPI': 'K', 'KYQ': 'K', 'LLP': 'K',
            'LYR': 'K', 'M3L': 'K', 'MEN': 'N', 'MIR': 'S', 'MLY': 'K',
            'MLZ': 'K', 'MSE': 'M', 'OCS': 'C', 'PCA': 'Q', 'PHD': 'D',
            'PTR': 'Y', 'SAC': 'S', 'SCH': 'C', 'SEP': 'S', 'SGB': 'S',
            'SMC': 'C', 'SME': 'M', 'SNC': 'C', 'SNM': 'S', 'SNN': 'N',
            'SUN': 'S', 'SVX': 'S', 'TPO': 'T', 'TYS': 'Y', 'YTH': 'T'}

#*************************************************************************
def amino_acid_code_converter(amino_acid):
    """
    input: amino_acid (string) - three letter amino acid code
    return: the corresponding one letter amino acid code
    V1.0   01.05.21  Original   By: Ayub Hareed
    """
    if (amino_acid in prot_seq.keys()):
        return (prot_seq[amino_acid])
    # if the amino acid code not found in the
    # look up dictionary prot_seq
    else:
        return ('X') 

#*************************************************************************
def read_encode_file(filename):
    """
    Input: filename(string)  - filename of the type of encode  
    returns: list (string list) - list of the encode file lines 
    V1.0   01.05.21  Original   By: Ayub Hareed
    """
    with open(filename, 'r') as f:
        # read in the file and remove \n 
        file_raw = f.read().splitlines()
        result = []
        for line in file_raw:
            if "#" not in line:
                result.append(line) 
    return (result)
#*************************************************************************
def secstr_encode(lst):
    """
    input: lst (list string) list of secondary structure encode from the 
    SeconaryStructure.txt file 
    returns: dictionary (values (encode))
    V2.0   10.06.21        By: Ayub Hareed
    """
    secstr_dict = {}
    encode = ''
    for line in lst:
        if len(line) > 0 and line[0] != ' ':
            score = [i for i in line[1:].split()]
            encode = ','.join(score)
            secstr_dict[line[0]] = encode
    return (secstr_dict)

#*************************************************************************
# BLOSUM62 score for each amino acid
def blosum_encode(lst,new=False):
    """
    input: lst (list string) list of blosum scores from the blosum file 
    returns: dictionary (values (interger list))
    V1.0   01.05.21  Original   By: Ayub Hareed
    """
    blosum_dict = {}
    blosum_sub_score = ''
    for line in lst:
        if (len(line) > 0 and line[0] != ' ' and new == False):
            score = [i for i in line[1:].split()]
            blosum_sub_score = ','.join(score[:20])  
            blosum_dict[line[0]] = blosum_sub_score
        elif (len(line) > 0 and line[0] != ' ' and new == True):
            if (len(line) > 20):
                score = [i for i in line[1:].split()]
                blosum_sub_score = ','.join(score[:24])
                blosum_dict[line[0]] = blosum_sub_score
    return (blosum_dict)

#*************************************************************************
def tscale5_or_abhinandan4_encode(lst):
    """
    input: lst (list string) list of scores for tscale5 or abhinandan4
    returns: dictionary (values (float list))
    V1.0   01.05.21  Original   By: Ayub Hareed
    """
    encode_dict = {}
    encode_str = ''
    for line in lst:
        if len(line) > 0 and line[0] != ' ':
            score = [float(i) for i in line[1:].replace(':', '').split()]
            encode_str = ','.join([str(i) for i in score])   
            encode_dict[line[0]] = encode_str
    return (encode_dict)

#*************************************************************************

class Encode:
    def __init__(self, path,encoder):
        self.path = path
        self.encoder = encoder
    
    def get_encode_dict(self):
        self.lst = read_encode_file(self.path)
        if 'blosum' in self.encoder:
            self.dict = blosum_encode(self.lst)
            return (self.dict)
        if 'tscale5' in self.encoder or 'abhinandan4' in self.encoder:
            self.dict = tscale5_or_abhinandan4_encode(self.lst)
            return (self.dict)
        if 'sec' == self.encoder:
            self.dict = secstr_encode(self.lst)
            return (self.dict)
        if 'a4nb90' in self.encoder and 'blosum' not in self.encoder:
            self.dict = blosum_encode(self.lst,new=True)
            return (self.dict)


#*************************************************************************
# read in encode files
# blosum45_list = read_encode_file('Encodings/data/BLOSUM45') # blosum62 encode file
# blosum62_list = read_encode_file(
#     'Encodings/data/BLOSUM62')  # blosum62 encode file
# blosum80_list = read_encode_file(
#     'Encodings/data/BLOSUM80')  # blosum62 encode file
# blosum90_list = read_encode_file('Encodings/data/BLOSUM90') # blosum62 encode file
# TScale5_list = read_encode_file('Encodings/data/TScale5.txt') # TScale5  encode file
# abhinandan4_list = read_encode_file('Encodings/data/Abhinandan4.txt') # TScale5  encode file


# # blosum encode dictionaries
# blosum45_dict = blosum_encode(blosum45_list)
# blosum62_dict = blosum_encode(blosum62_list)
# blosum80_dict = blosum_encode(blosum80_list)
# blosum90_dict = blosum_encode(blosum90_list)

# # TScale5 encode dictionary
# tscale5_dict = tscale5_or_abhinandan4_encode(TScale5_list)


# #  abhinandan4 encode dictionary
# abhinandan4_dict = tscale5_or_abhinandan4_encode(abhinandan4_list)





# below are testing codes  


# def file_readin(filename):
#     with open(filename, 'r') as f:
#         csv_file = csv.reader(f)
#         file_list = [i for i in csv_file]
#     return file_list

# def line_print(line_lst):
#     line = ''
#     for i, lst in enumerate(line_lst):
#         line += lst[0] + ',' + lst[1] + ',' + lst[2] + ','  
#         for aa in lst[3:]:
#             if aa != lst[-1]:
#                 line += amino_acid_code_converter(aa) + ','
#             else:
#                 line += amino_acid_code_converter(aa)
#         line += '\n'
#     return print(line)

# file = sys.argv[1]
# csv_lst = file_readin(file)

# line_print(csv_lst)
