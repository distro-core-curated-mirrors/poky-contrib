#!/bin/bash

# TODO
# * the apt-get commands just run once and not every time vagrant provisions
# * set the env varirables from Vagrantfile instead of hardcoding it on this file

# patchtest requirements
sudo apt-get update
sudo apt-get install -y git python python-virtualenv python-pip

# Define the following variables
REPODIR=""   #<Define where you want the repository to be located>
REPOURL=""   #<Define the repository's git URL>
PWURL=""     #<Define where the Patchwork's URL>
PWPROJECT="" #<Define patchwork's related project>
PWUSER=""    #<Define the Patchwork's user>
PWPASS=""    #<Define the PWUSER's password>

# install poky repository and configure it
/vagrant/patchtest/scripts/setup-repodir.sh \
    $REPODIR \
    $REPOURL \
    $PWURL \
    $PWPROJECT \
    $PWUSER \
    $PWPASS

# execute patchtest
/vagrant/patchtest/scripts/run-patchtest.sh $REPODIR
