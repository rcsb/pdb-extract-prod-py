#!/usr/bin/env bash

pythonVersion=3.12

webBaseDir=/data/wwpdb/pdb_extract_service/pdb-extract-web

source ${webBaseDir}/venv/bin/activate

pythonExe=python${pythonVersion}

${pythonExe} -m pip install --upgrade pip

# ${pythonExe} -m pip install six
# ${pythonExe} -m pip install scikit-build
${pythonExe} -m pip install cmake
${pythonExe} -m pip install mmcif


runUser=wwwdev

scrDir=`dirname ${0}`
scrAbsDir="`( cd \"${scrDir}\" && pwd )`"

runuser -l ${runUser} -c "cd ${scrAbsDir}; ./install.sh"

