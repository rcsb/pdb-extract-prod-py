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
		echo "[*] Change directory to Maxit installation folder of"
		cd $PDB_EXTRACT_PY/packages
		pwd
	endif
endif

set maxit_name="maxit-v11.100-prod-src"
set maxit_filename=${maxit_name}.tar.gz
set url_maxit=https://sw-tools.rcsb.org/apps/MAXIT/$maxit_filename
echo "[*] Downloading Maxit suite from \e[93m${url_maxit}\e[0m"

if (-f $maxit_filename) then
	echo "[*] file \e[93m${maxit_filename}\e[0m already exists, skipping download"
else
	curl $url_maxit -O
endif

echo "[*] File \e[93m${maxit_filename}\e[0m downloaded"
echo "[*] Decompressing \e[93m${maxit_filename}\e[0m starts"
tar -zxvf $maxit_filename
echo "[*] Decompressing \e[93m${maxit_filename}\e[0m finished"

echo "[*] Maxit installation starts"
cd $PDB_EXTRACT_PY/packages/$maxit_name
pwd
make binary
echo "[*] Maxit installation finished"
