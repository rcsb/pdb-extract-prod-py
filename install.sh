#!/usr/bin/env bash

## For Bourne shell users:

function download_file {
    local url=$1
    local filename="${url##*/}"

    if [[ ! -f "$filename" ]]; then
        curl $url -O
    else
        echo "[*] file ${filename} already exists, skipping download"
    fi
}

read maxit_version < "maxit_latest_version"
echo "[*] Get Maxit latest version ${maxit_version}"
maxit_name=maxit-${maxit_version}-prod-src
maxit_filename=${maxit_name}.tar.gz
echo "[*] Get Maxit package name ${maxit_filename}"
url_maxit=https://sw-tools.rcsb.org/apps/MAXIT/$maxit_filename
echo "[*] Get download URL of ${url_maxit}"

if [ ! -d packages ]
then
echo "[*] To make packages folder"
mkdir packages
else
echo "[*] Packages folder exists"
fi
echo "[*] To change directory to Maxit installation folder"
cd packages

echo "[*] Start to download Maxit suite from ${url_maxit}"
download_file $url_maxit
echo "[*] Finish downloading ${maxit_filename}"
echo "[*] Start to decompress ${maxit_filename}"
#tar -zxvf $maxit_filename
echo "[*] Finish decompressing ${maxit_filename}"
echo "[*] Start to install Maxit"
#cd $maxit_name
#make binary

cd ../..
echo "[*] Finish installating Maxit"
