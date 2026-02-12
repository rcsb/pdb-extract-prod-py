#!/usr/bin/env bash

python3 -m pip install --upgrade pip
# python3 -m pip install six
# python3 -m pip install scikit-build
python3 -m pip install cmake
python3 -m pip install mmcif==0.92.0


runUser=wwwdev

scrDir=`dirname ${0}`
scrAbsDir="`( cd \"${scrDir}\" && pwd )`"

runuser -l ${runUser} -c "cd ${scrAbsDir}; ./install.sh"

