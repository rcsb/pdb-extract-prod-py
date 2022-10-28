#!/usr/bin/env csh
## For C shell users:
## Must run "source setup.csh" before executing this script to set up enviroment variables.

if (! $?PDB_EXTRACT_PY) then       
	echo "[*] Please run source setup.sh before executing this script"
	exit 1
else
	if ("$PDB_EXTRACT_PY" == "") then
		echo "[*] Please run source setup.sh before executing this script"
		exit 1
	else
		echo "[*] Change directory to dictionary folder of"
		cd $PDB_EXTRACT_PY/data/dictionary
		pwd
	endif
endif

set dict_filename="mmcif_pdbx_v5_next.dic.gz"
if (-f $dict_filename) then
	echo "[*] file \e[93m${dict_filename}\e[0m already exists, removing old file"
	rm $dict_filename
endif

set url_dict=https://mmcif.wwpdb.org/dictionaries/ascii/$dict_filename
echo "[*] Downloading latest mmCIF dictionary from \e[93m${url_dict}\e[0m"
curl $url_dict -O
echo "[*] Decompressing \e[93m${dict_filename}\e[0m"
gunzip -f $dict_filename
echo "[*] mmCIF dictionary file has been updated"
