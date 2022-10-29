#!/usr/bin/env bash

python3 -m pip install six

runUser=wwwdev

scrDir=`dirname ${0}`
scrAbsDir="`( cd \"${scrDir}\" && pwd )`"

runuser -l ${runUser} -c ". ${scrAbsDir}/setup.sh; ${scrAbsDir}/install.sh"

