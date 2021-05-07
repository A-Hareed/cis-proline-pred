#!/usr/bin/python3
"""
...header to be added...
"""
import re
import config


#read in torsion angle files from pdbtorsions
path = input(str())

#**************************************************************
def proline_extr(path):
    with open(path, 'r') as f:
        index_dict = {}
        raw_file = f.read().splitlines()
        for num, line in enumerate(raw_file):
            if num >1:
                #indexing them to take flagging sequences
                i = num -2
                line = re.sub(r'\s+', '|',line)
                lst = line.split('|')
                index_dict[i] = lst[:2] + [lst[4]]

    final_dict = {}
    for k, v in index_dict.items():
        upstream_seq = []
        downstream_seq = []
        ustr = ''
        dstr = ''

        
        if v[1] == 'PRO':
            #obtain torsion angle
            pre_atom = index_dict[k-1]
            torsion_str = pre_atom[2]
            torsion = abs(float(torsion_str))
            if torsion > 160 and torsion < 185:
                form = 'trans'
            else:
                form = 'cis'

            #obtain flanking sequence
            downstream_keys = [(k - i) for i in range(0,4)]
            upstream_keys = [(k + i) for i in range(0, 4)]
            upstream_keys.reverse()
            
            #lst1 = [index_dict.get(key) for key in upstream_keys]
            #getting upstream sequence 
            for key in upstream_keys:
                if key != k:
                    A = index_dict.get(key)

                   #change three letter code to one letter
                    one_code = config.prot_seq[A[1]]
                    upstream_seq.append(one_code)
                    ustr = ''.join(upstream_seq)

            #getting downstream sequence
            for key in downstream_keys:
                if key != k:
                    A = index_dict.get(key)

                    #change three letter code to one letter
                    one_code = config.prot_seq[A[1]]
                    downstream_seq.append(one_code)
                    dstr = ''.join(downstream_seq)
            final_dict[v[0]] = [ustr,form,dstr] 
        #print(k, lst1)
    return final_dict
#**************************************************************
def to_csv(tor, pdb):
    #csv_line = "pdb,atom num,type,upstream seq,downstream\n" 
    for k, v in tor.items():
        csv_line += pdb+ ',' + k + ',' + v[1] + ',' + v[0] + ',' + v[2] + '\n'
    return csv_line

#**************************************************************

#extract pdb name and create export path
str_path = path
p = re.compile(r'[/a-zA-Z_-]+/([0-9A-Za-z]+)')
p2 = re.compile(r'([/a-zA-Z_-]+)/(torsion)')
match= p.search(str_path)
match2= p2.search(str_path)
pdb_name = match.group(1)

export_path = match2.group(1) + "/dataset"

cis_proline_dict = proline_extr(path)

print(to_csv(cis_proline_dict,pdb_name))


