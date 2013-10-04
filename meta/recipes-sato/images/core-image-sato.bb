DESCRIPTION = "Image with Sato, a mobile environment and visual style for \
mobile devices. The image supports X11 with a Sato theme, Pimlico \
applications, and contains terminal, editor, and file manager."

<<<<<<< HEAD
IMAGE_FEATURES += "splash package-management x11-base x11-sato ssh-server-dropbear hwcodecs"
=======
IMAGE_FEATURES += "splash package-management x11-base x11-sato ssh-server-dropbear"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

LICENSE = "MIT"

inherit core-image

IMAGE_INSTALL += "packagegroup-core-x11-sato-games"
