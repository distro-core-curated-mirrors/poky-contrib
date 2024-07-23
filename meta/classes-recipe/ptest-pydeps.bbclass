# Lowest-possible useful test case for python modules.
# This simply imports the modules to verify that they are importable.

inherit ptest

# The list of modules that will be imported, to verify dependencies
PTEST_PYDEPS_MODULES ?= "${PYPI_PACKAGE}"

# TODO definitely terrible as it doesn't recurse as it should. use importlib to find files in a named distro and import every one?

write_run_ptest() {
	cat <<-'EOF' >${UNPACKDIR}/run-ptest
	#! /bin/sh
	set -eu
	for MODULE in ${PTEST_PYDEPS_MODULES}; do
	    python3 -c "import $MODULE" && echo PASS: $MODULE || echo FAIL: $MODULE
	done
	EOF
}
do_unpack[postfuncs] += "write_run_ptest"
