#!/usr/bin/env bash

## For Bourne shell users:
## Must run "source setup.sh" before executing this script to set up enviroment variables.

function highlight_text {
    echo -ne "\e[93m$1\e[0m"
}

function download_file {
    local url=$1
    local filename="${url##*/}"

    if [[ ! -f "$filename" ]]; then
        curl $url -O
    else
        echo "[*] file $(highlight_text $filename) already exists, skipping download"
    fi
}

if [ -z "$PDB_EXTRACT_PY" ] 
then
    echo "[*] Please run source setup.sh before executing this script"
	exit 1
else 
	echo "[*] Change directory to Maxit installation folder of"
	cd $PDB_EXTRACT_PY/packages
	pwd
fi

maxit_name="maxit-v11.100-prod-src"
maxit_filename=${maxit_name}.tar.gz
url_maxit=https://sw-tools.rcsb.org/apps/MAXIT/$maxit_filename
echo "[*] Downloading Maxit suite from $(highlight_text $url_maxit)"
download_file $url_maxit
echo "[*] File $(highlight_text $maxit_filename) downloaded"
echo "[*] Decompressing $(highlight_text $maxit_filename) starts"
tar -zxvf $maxit_filename
echo "[*] Decompressing $(highlight_text $maxit_filename) finished"
echo "[*] Maxit installation starts"
cd $PDB_EXTRACT_PY/packages/$maxit_name
pwd
make binary
echo "[*] Maxit installation finished"

