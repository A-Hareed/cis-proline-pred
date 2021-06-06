#! /usr/bin/python3

# import libraries
import sys

#***********************************************
def read_file(filename):
    with open(filename, 'r') as f:
        file_list = f.read().splitlines()
    return (file_list)

#***********************************************
def get_pdd_name(pdb_dataset):
    pdb_dataset = pdb_dataset[1:]
    
    pdb_lst = []
    results = []
    for line in pdb_dataset:
        temp_lst = line.split()
        
        pdb_lst.append(temp_lst)
    
    for line in pdb_lst:
        results.append(line[0])
    return (results)


#***********************************************
def find_pdb(quiery, pdb_dataset):
    quiery_lst = []

    pdb_dataset = ["pdb" + i[:4].lower() for i in pdb_dataset]
    result = ''
    lst_results = []
    for i in quiery:
        lst = i.split()
        quiery_lst.extend(lst)
    
    for cull_pdb in pdb_dataset:
        #cull_pdb = cull_pdb[:-1]
        for i in quiery_lst:
            if (cull_pdb in i):
                result += i + " "
                lst_results.append(i)
                
    
    return (lst_results)

#***********************************************
#       main program
#***********************************************
if (len(sys.argv) >= 2):
    #quiery_file = sys.argv[2]
    #quiery_raw = read_file(quiery_file)
    database = read_file(sys.argv[1])
    cleaned_dataset = get_pdd_name(database)
   # print(len(cleaned_dataset))
    #quiery = find_pdb(quiery_raw, cleaned_dataset)
    #print(f"final out put len: {len(quiery)}")
    clean_clean = ["pdb" + i[:4].lower() for i in cleaned_dataset]
    result = ""
    for i in clean_clean:
        result += i + " "
    print(result)
    # set1 = set(clean_clean)
    # set2 = set(quiery)
    # z = set1.difference(set2)
    # print(len(z))
    # print("ok")
    # print(quiery)
