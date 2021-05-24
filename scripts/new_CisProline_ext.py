#! /usr/bin/python3
import os 
import config # lookup table for single letter amino acid code
import re

os.chdir('/home/ayub/Desktop/cis_proline/cis-proline-pred/torsion') # changes directory

file_names = os.listdir()  # gets file names ***if you whant to test with one torsion than use ['name'] 


for file in file_names: #loops through torsion files
    with open(file, 'r') as f:
        torsion_list_raw = f.read().splitlines() # reads text file as a list where each line is the item
        torsion_list = [tuple(i.split()) for i in torsion_list_raw] # splits each line into items 
        torsion_list = torsion_list[2:]    # removes header

        for i, tup in enumerate(torsion_list): #loop through list
            data_rows, form, no_flank, kmer = [], '', False, 3      #varibles and list set up
            if i > 1:
                if tup[1] == "PRO" and (i + kmer) <= (len(torsion_list)-1) and (i - kmer) >= 0:
                    kmer_range = range(1, (kmer+1)) # create range to extract flanking sequence
                    upstream_seq = [torsion_list[i + k][1] for k in kmer_range]
                    downstream_seq = [torsion_list[i - k][1] for k in reversed(kmer_range)]
                    #test if simple amino acid present
                    for num in range(0,kmer):
                        aa_test1 = [False if aa not in config.prot_seq.keys() else True for aa in  upstream_seq]
                        aa_test2 = [False if aa not in config.prot_seq.keys() else True for aa in  downstream_seq]
                    # get torsion angle
                    angle = abs(float(tup[-1]))
                    # regex for pdb name 
                    pdb_match = re.search(r'[/a-zA-Z_-]*([a-zA-Z0-9\_]+)\.', file) 
                    pdb_name = pdb_match.group(1)   
                    if angle > 90:
                        form = 'trans'
                    else:
                        form = 'cis'  # when proline is found n-1 it has a small angle but this can't be considered as a cis-proline

                    if False in aa_test1 or False in aa_test2 or angle == 9999.000: # prevents none simple amino acids causing errors and flanking seq
                        continue						    # that overlaps two chains

                    elif torsion_list[i+kmer][0][0] != tup[0][0] or torsion_list[i-kmer][0][0] != tup [0][0]:
                        continue

                    else:    
                        # csv print format
                        print_statment = [pdb_name] + [tup[0]] + [config.prot_seq[aa] for aa in downstream_seq] + ['PRO'] + \
                                        [config.prot_seq[aa] for aa in upstream_seq] \
                                        + [form] + [angle]

                        for statement in print_statment: # just prints out the output e.g. E,K,Q,PRO,P,L,V,trans
                            if statement != print_statment[-1]:
                                print(f'{statement},', end='')
                            else:
                                print(statement)
        




