file_prefix_map_option () {
	# Check if KERNEL_CC supports the option "file-prefix-map".
	# This option allows us to build images with __FILE__ values that do not
	# contain the host build path.
	if ${KERNEL_CC} -Q --help=joined | grep -q "\-ffile-prefix-map=<old=new>"; then
		echo "-ffile-prefix-map=${S}=/${BP}/"
	fi
}
