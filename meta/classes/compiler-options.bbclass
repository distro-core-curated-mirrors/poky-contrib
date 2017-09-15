
file_prefix_map_option_supported () {
	# Check if CC supports the option "file-prefix-map".
	# This option allows us to build images with __FILE__ values that do not
	# contain the host build path.
	if $1 -Q --help=joined | grep -q "\-ffile-prefix-map=<old=new>"; then
		echo "-ffile-prefix-map=${S}=/${BP}/"
	fi
}
