LICENSE = "MIT"
IMAGE_FEATURES += "splash"
inherit core-image

IMAGE_INSTALL += "docker docker-contrib"
IMAGE_INSTALL += "connman connman-client"

