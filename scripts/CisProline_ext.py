#!/usr/bin/python3
"""
...header to be added...
"""
import re


#read in torsion angle files from pdbtorsions
#path = '../torsion/1cuk.txt'

#path = '/home/ayub/Desktop/cis_proline/cis-proline-pred/torsion/1cuk.txt'

path = input(str())

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
        config = ''
        if v[1] == 'PRO':
            #obtain torsion angle
            pre_atom = index_dict[k-1]
            torsion_str = pre_atom[2]
            torsion = abs(float(torsion_str))
            if torsion > 160 and torsion < 185:
                config = 'trans'
            else:
                config = 'cis'

            #obtain flanking sequence
            downstream_keys = [(k - i) for i in range(0,4)]
            upstream_keys = [(k + i) for i in range(0, 4)]
            upstream_keys.reverse()
            
            #lst1 = [index_dict.get(key) for key in upstream_keys]
            #getting upstream sequence 
            for key in upstream_keys:
                if key != k:
                    A = index_dict.get(key)
                    upstream_seq.append(A[1])
            #getting downstream sequence
            for key in downstream_keys:
                if key != k:
                    A = index_dict.get(key)
                    downstream_seq.append(A[1])
            final_dict[v[0]] = upstream_seq + [config] + downstream_seq 
        #print(k, lst1)
    return final_dict
print(proline_extr(path))


