#!/usr/bin/env bash

# A portion of the whole PdbExtract system is relying on system python3
# environment. That is why this environment needs to be set up here:

python3 -m pip install --upgrade pip

# python3 -m pip install six
# python3 -m pip install scikit-build
python3 -m pip install cmake
python3 -m pip install mmcif==0.92.0


# A portions of the whole PdbExtract system is relying on custom python3
# environment. That is why this environment needs to be set up here:

runUser=wwwdev

pythonVersion=3.12
webBaseDir=/data/wwpdb/pdb_extract_service/pdb-extract-web

sudo -u ${runUser} bash -c "
    source ${webBaseDir}/venv/bin/activate

    pythonExe=python${pythonVersion}

    \${pythonExe} -m pip install --upgrade pip

    # \${pythonExe} -m pip install six
    # \${pythonExe} -m pip install scikit-build
    \${pythonExe} -m pip install cmake
    \${pythonExe} -m pip install mmcif
"


scrDir=`dirname ${0}`
scrAbsDir="`( cd \"${scrDir}\" && pwd )`"

runuser -l ${runUser} -c "cd ${scrAbsDir}; ./install.sh"

