#
# ${PN}-bin is defined in bitbake.conf
#
# We need to allow the other packages to be greedy with what they
<<<<<<< HEAD
# want out of /usr/bin and /usr/sbin before ${PN}-bin gets greedy.
=======
# want out of /bin and /usr/bin before ${PN}-bin gets greedy.
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
# 
PACKAGE_BEFORE_PN = "${PN}-bin"
