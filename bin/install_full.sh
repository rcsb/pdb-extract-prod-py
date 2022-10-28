#!/usr/bin/env bash

scrDir=`dirname ${0}`
scrAbsDir="`( cd \"${scrDir}\" && pwd )`"

. ${scrAbsDir}/setup.sh

${scrAbsDir}/install.sh

