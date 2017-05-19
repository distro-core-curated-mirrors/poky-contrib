LICENSE = "MIT"
inherit core-image
IMAGE_FEATURES += "ssh-server-openssh"
IMAGE_INSTALL += "docker docker-contrib"
IMAGE_INSTALL += "connman connman-client"

