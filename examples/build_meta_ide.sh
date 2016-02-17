#!/bin/bash
#$1
cd $1
source oe-init-build-env build
bitbake -c cleansstate meta-ide-support
bitbake meta-ide-support

