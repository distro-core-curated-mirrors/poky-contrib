EXTRANATIVEPATH += "pigz-native gzip-native"
DEPENDS += "gzip-native"

<<<<<<< HEAD
# tar may get run by do_unpack or do_populate_lic which could call gzip
do_unpack[depends] += "gzip-native:do_populate_sysroot"
=======
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
