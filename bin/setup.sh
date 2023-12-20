#!/bin/env bash

## For Bourne shell users:
## ========== source this file before execute the program========
##
## Only need to modify the 1st row of the content by replacing the
## directory with the full directory of your PDB-Extract folder
## e.g. export PDB_EXTRACT_PY=/home/username/pdb-extract-prod-py

## export PDB_EXTRACT_PY=/Users/chenghua/Projects/pdb-extract-prod-py
export PDB_EXTRACT_PY=/Users/chenghua/Projects/pdb-extract-prod-py
export RCSBROOT=$PDB_EXTRACT_PY/packages/maxit-v11.100-prod-src
export PATH=$PDB_EXTRACT_PY/bin:$PATH
if [ -z "$PYTHONPATH" ] 
then
    ## echo "variable is empty"
	export PYTHONPATH=$PDB_EXTRACT_PY
else 
    ## echo "variable has value"
	export PYTHONPATH=${PDB_EXTRACT_PY}:$PYTHONPATH
fi

cd $PDB_EXTRACT_PY/bin
chmod a+x install.sh
chmod a+x updateDictionary.sh
chmod a+x pdb_extract.py
chmod a+x pdb_extract_cgi.py
chmod a+x mergeTwoTemplates.py



