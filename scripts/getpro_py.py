#!/usr/bin/python3
#*************************************************************************
#
#   Program:    getpro
#   File:       getpro.py
#   
#   Version:    V1.0
#   Date:       10.05.21
#   Function:   Extract proline information and a window of residues from
#               the output of pdbtorsions
#   
#   Copyright:  (c) Prof. Andrew C. R. Martin, UCL, 2021
#   Author:     Prof. Andrew C. R. Martin
#   Address:    Institute of Structural and Molecular Biology
#               Division of Biosciences
#               University College
#               Gower Street
#               London
#               WC1E 6BT
#   EMail:      andrew@bioinf.org.uk
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
#   V1.0   10.05.21  Original   By: ACRM
#   V2.0   10.05.21             By: Ayub Hareed
#*************************************************************************
# Import libraries
import sys
import os 
import utilities # used to convert three letter amino acid code to one letter code
# ------------------------------------------------------------------------
def basename(filename):
    """
    Input:   (string) filename - a filename
    Returns: (string) the base filename (with extension and path removed)

    Removes the path and extension from a filename

    10.05.21 Original By: ACRM
    07.06.21       v3 by: Ayub Hareed 
    """
    # Remove the file extension
    offset = filename.rfind('.')
    if(offset >= 0):
        filename = filename[:offset]

    # Remove the path
    offset = filename.rfind('/')
    if(offset >= 0):
        filename = filename[offset+1:]
    
    underscr =  filename.rfind('_')
    if (underscr >= 0):
        filename = filename[:underscr]

    return(filename)

# ------------------------------------------------------------------------
def read_file(filename):
    """
    Input:   (string) filename - a filename
    Returns: (string list) a list containing the contents of the file

    Reads a file into a list

    10.05.21 Original By: ACRM
    """
    data = []
    with open(filename, 'r') as infile:
        for line in infile:
            data.append(line.rstrip())
            
    return(data)

# ------------------------------------------------------------------------
def check_cis_trans(dataline):
    """
    Input:   (string) dataline - a line from the output of pdbtorsions
    Returns: (string) 'cis', 'trans' or ''

    Identifies whether the amino acid in cis, trans or undefined.

    10.05.21 Original By: ACRM
    """
    fields = dataline.split()
    omega  = abs(float(fields[4]))

    if(omega > 9998.0):
        return('')
    
    if(omega > 90.0):
        return('trans')
    
    return('cis')

# ------------------------------------------------------------------------

def process_a_proline(data, window, line_number):
    """
    Input:   data (string list)    - the pdbtorsions file contents
             window (integer)      - the window size - actually the number
                                     of amino acids to look at each side 
                                     of the proline
             line_number (integer) - the index into the data array for 
                                     the current proline
    Returns: (string) the results for this proline or a blank string if
             the proline is too close to the end of a chain or has an
             undefined omega torsion angle

    Constructs the result CSV string for the current proline. This is the
    filestem:resid followed by cis/trans and the list of amino acids
    before and after the proline

    10.05.21 Original By: ACRM
    10.05.21 v.2.0    By: Ayub Hareed
    """
    
    # To store the results
    result = ''
    
    # See how many data points we have so we don't go off the end
    data_size = len(data)

    # Find which chain we are in for the specified line of data (this
    # is the first character of the data line)
    the_line  = data[line_number]
    the_chain = the_line[0]

    # Find the residue label (this is the first field of the data line)
    fields    = the_line.split()
    the_label = fields[0]
    # Add this to the result
    result    = result + the_label

    # See if this residue is cis or trans
    cistrans  = check_cis_trans(data[line_number])
    if(cistrans == ''):
        return('')
    # Add this to the result
    result    = result + ',' + cistrans # seperated this by ',' to have two coloumns in csv
    
    # Step from 'window' before the current line to 'window' after the
    # current line
    current_line_number = line_number - window
    while(current_line_number <= line_number + window):
        # If we are outside the data, return a blank string
        if((current_line_number < 0) or
           (current_line_number >= data_size)):
            return('')
        # If the chain label isn't the same as our key residue, return
        # a blank string
        this_line  = data[current_line_number]
        this_chain = this_line[0]
        fields     = this_line.split()
        if (len(fields) > 1): 
            this_residue = fields[1]
            # uses function from utilities to convert three letter amino acid code 
            # to one letter
            one_letter = utilities.amino_acid_code_converter(this_residue)
        elif (len(fields) <= 1):
            return ('')
        if(this_chain != the_chain):
            return('')

        if (one_letter == 'X'):
            return ('')

        # Append the data for this residue (unless it's the proline)
        if(current_line_number != line_number):
            result = result + ',' + one_letter

        # Increment the line count
        current_line_number = current_line_number + 1
        
    return(result)
        

# ------------------------------------------------------------------------
def find_prolines(data, window):
    """
    Input:   data (string list) - the contents of the pdbtorsions output
             window (integer)   - the window size - actually the number
                                  of amino acids to look at each side of
                                  the proline
    Returns: (string list) the results for all (valid) prolines in the
             file. Each item is a CSV type line. Note that the filename
             is not included in the first field.

    10.05.21 Original By: ACRM

    """
    results      = []
    line_number  = 0

    for line in data:
        # Ignore comment lines
        if (len(line) > 1):
            if(line[0] != '#'):
                fields = line.split()
                if(fields[1] == 'PRO'):
                    result = process_a_proline(data, window, line_number)
                    if(result != ''):
                        results.append(result)
            line_number = line_number + 1
    return(results)

# ------------------------------------------------------------------------
def getsecstrc(directory=None):
    files_lst = os.listdir(directory)  # list directories
    results = {} 
    if directory != None:
        for file in files_lst:
            # Read the data file (output of pdbtorsions)
            file = directory + '/' + file
            fileid = basename(file)

            with open(file, 'r') as f:
                raw_lst = f.read().splitlines()
                sec_lst = [i.split() for i in raw_lst]
            for line in sec_lst:
                key = fileid + ',' + line[0]
                results[key] = line[-1]
    else:
        results = ''
    return (results)




# ------------------------------------------------------------------------
def file_input(filename, window, strc_dir=None):
    """
    input: filename (string) - pdbtorsions output file name 

    returns:  
    18.05.21    v2.0 By: ACRM
    18.05.21    v2.0 By: Ayub Hareed
    """
    results = ''
    # Read the data file (output of pdbtorsions)
    data    = read_file(filename)
    # Get the file id
    fileid = basename(filename)

    # Extract the proline information and 
    # prepend the filename on each line
    for result in find_prolines(data, window):
        if strc_dir != None:
            # finds atom number
            result_lst = result.split(',')
            atom_num = result_lst[0]
            # generates a dictionary for proline secondary structure
            secstr = getsecstrc(strc_dir)
            key = fileid + ',' + atom_num
            if key in secstr.keys():
                sec = ',' + '*' + secstr[key]
            else:
                no_sec = f'this pdb had no secondary structure info: {key}'
                with open('/home/ayub/Desktop/cis_proline/pisces/test/cathe.out', 'a') as f:
                    f.write(f'{no_sec}\n')
                continue

        else:
            sec = ''

        results += fileid + ',' + result + sec + '\n'
    return (results)

# ------------------------------------------------------------------------
def directory_input(directory, window, strc_dir = None):
  """
  Input: directory (string) - directory path where pdbtorsions output are

  returns: (string)         - prints proline results for multiple pdb 
                              files.

  18.05.21    v2.0 By: Ayub Hareed
  """
  files_lst = os.listdir(directory)  # list directories     
  results = '' 
  for file in files_lst:
      # Read the data file (output of pdbtorsions)
      file = directory + '/' + file
      data = read_file(file) 
      # Get the file id
      fileid = basename(file)

      #  results - prepending the filename to each line
      for result in find_prolines(data, window):
          if strc_dir != None:
            # finds atom number
            result_lst = result.split(',')
            atom_num = result_lst[0]
            # generates a dictionary for proline secondary structure
            secstr = getsecstrc(strc_dir)
            key = fileid + ',' + atom_num
            if key in secstr.keys():
                sec = ',' + '*' + secstr[key]
            else:
                no_sec = f'this pdb had no secondary structure info: {key}'
                with open('/home/ayub/Desktop/cis_proline/pisces/test/cathe.out', 'a') as f:
                    f.write(f'{no_sec}\n')
                continue
          else:
            sec = ''
          results += fileid + ',' + result + sec + '\n'
    
  return (results)


# ------------------------------------------------------------------------
def usage_die():
    """
    Prints a usage message and exits the program

    10.05.21 Original By: ACRM
    V2.0   10.05.21             By: Ayub Hareed

    """
    print ("""
getpro V1.0 (c) UCL, Prof. Andrew C.R. Martin
getpro V2.0 (c) UCL, Ayub Hareed

Usage: getpro pdbtorsions.txt [halfwindow]
       pdbtorsions.txt - the output from pdbtorsions
       halfwindow      - the half-window size - i.e. how many residues 
                         before and after a proline that we look at.
                         [Default: 3]

getpro extracts all the prolines from the output of pdbtorsions and 
identifies whether they are cis or trans. This information is output
as a CSV file together with the residues 'halfwindow' before and after
the proline. Prolines fewer than halfwindow amino acids from the end
of a chain are not output.

input parameters:

-f [filename] :the '-f' parameter reads in file names which are pdbtorsions.txt 
                (the output from pdbtorsions)

-d [directory name] :the '-d' parameter reads in the pdbtorsions.txt (the output from pdbtorsions)
                      in the given directory 
""")
    sys.exit()



# ------------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------------

# Read the command line
# If '-h' or wrong number of arguments, print usage message and exit
if((len(sys.argv) > 7) or
   (len(sys.argv) < 3) or
   (sys.argv[1] == '-h') or
   sys.argv[1] not in ['-f', '-d']):
    usage_die()



window = 3
if ('-w' in sys.argv):
    i = sys.argv.index('-w')
    window = int(sys.argv[i+1])


if ('-s' in sys.argv):
    i = sys.argv.index('-s')
    sec_dir = sys.argv[i+1]
else:
    sec_dir = None


if (sys.argv[1] == '-f'):
    # extract proline information from file
    torsions_file = sys.argv[2]
    proline_results = file_input(torsions_file, window, sec_dir)
    print(proline_results)


if (sys.argv[1] == '-d'):
    # extract proline information from directory
    directory = sys.argv[2]
    proline_results = directory_input(directory, window, sec_dir)
    print(proline_results)





#----------------------------------------------------------------------------
#   old version
#----------------------------------------------------------------------------

# 
# if(len(sys.argv) == 4):
#     window = int(sys.argv[3])

# # Read the data file (output of pdbtorsions)
# data    = read_file(torsions_file)

# # Extract the proline information
# results = find_prolines(data, window)

# # Get the file id
# fileid  = basename(torsions_file)

# # Print the results - prepending the filename to each line
# for result in results:
#     print (fileid + ',' + result)


