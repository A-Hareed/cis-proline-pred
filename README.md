# Using Machine Learning to predict Cis/trans-proline:

ML tools like Weka and XGBoost are used to train the binary classifier to predict wether a amino acids attached to prolines have cis (0 degree)
omega-angle (ω) or trans (180 deree).


To do this, a protein dataset is built using a file listing all PDB chains used:

```
# see protein dataset 
less pdb/cullpdb_pc25.0_res0.0-3.0_noBrks_noDsdr_len40-10000_R0.25_Xray_d2021_06_05_chains3940
```

Using the script `scripts/pdb_database_build.sh`, the correct protein chains are extracted and the torsion angles are extracted into a text file by
the pdbtorsions which is part of the BiopTools (extras torsion all torsion angles from a PDB file):
```
# example of how pdbtorsions is used
pdbtorsions example_pdb_file.ent > torsion_file.txt
```


Once the torsion files are created for each pdb file the proline dataset csv file is made using the `scripts/getproline_py.py` program:

```
# extracting the proline datasets using 
# a directory that contains all torsion files

scripts/./getpro_py.py -d <directory with torsion>  -w <an intiger for window size> > proline_dataset.csv
```

Once the proline datasets are exracted to a single csv file its encoded using the encoder program `scripts/encoder.py` with the choice of an encoder e.g. BLOSUM90


