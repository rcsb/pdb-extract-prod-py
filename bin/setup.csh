#!/bin/env csh

## For C shell users:
## ========== source the file before execute the program========
##
## Only need to modify the 1st row of the content by replacing the
## directory with the full directory of your PDB-Extract folder
## e.g. setenv PDB_EXTRACT_PY /home/username/pdb-extract-prod-py

setenv PDB_EXTRACT_PY /data/wwpdb/pdb_extract_service/pdb-extract-prod-py
setenv RCSBROOT $PDB_EXTRACT_PY/packages/maxit-v11.100-prod-src
setenv PATH $PDB_EXTRACT_PY/bin:$PATH
if (! $?PYTHONPATH) then       
	## echo "variable is undefined"
	setenv PYTHONPATH $PDB_EXTRACT_PY
else
	if ("$PYTHONPATH" == "")  then
		## echo "variable is empty"
		setenv PYTHONPATH $PDB_EXTRACT_PY
	else 
		## echo "variable has value"
		setenv PYTHONPATH ${PDB_EXTRACT_PY}:$PYTHONPATH
	endif
endif

cd $PDB_EXTRACT_PY/bin
chmod a+x install.csh
chmod a+x updateDictionary.csh
chmod a+x pdb_extract.py
chmod a+x pdb_extract_cgi.py
chmod a+x mergeTwoTemplates.py
