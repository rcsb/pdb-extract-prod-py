#!/usr/bin/env bash

pythonVersion=3.12

pythonExe=/usr/bin/python${pythonVersion}

yum -y install python${pythonVersion}-pip

${pythonExe} -m pip install --upgrade pip
# ${pythonExe} -m pip install six
# ${pythonExe} -m pip install scikit-build
${pythonExe} -m pip install cmake
${pythonExe} -m pip install mmcif


runUser=wwwdev

scrDir=`dirname ${0}`
scrAbsDir="`( cd \"${scrDir}\" && pwd )`"

runuser -l ${runUser} -c "cd ${scrAbsDir}; ./install.sh"

