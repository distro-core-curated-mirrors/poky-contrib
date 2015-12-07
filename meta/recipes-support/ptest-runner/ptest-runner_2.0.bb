SUMMARY = "A python script to run all installed ptests"

DESCRIPTION = "The ptest-runner package installs a ptest-runner \
python script which loops through all installed ptest test suites and \
runs them in sequence."

HOMEPAGE = "https://wiki.yoctoproject.org/wiki/Ptest"
SRC_URI += "file://ptest-runner_2.0.py"

LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=4d92cd373abda3937c2bc47fbc49d690 \
                    file://${COREBASE}/meta/COPYING.GPLv2;md5=751419260aa954499f7abaabaa882bbe"

INHIBIT_DEFAULT_DEPS = "1"
RDEPENDS_${PN} = "python python-fcntl python-argparse python-logging python-datetime \
                  python-subprocess"

S = "${WORKDIR}"

do_install () {
    install -D -m 0755 ${WORKDIR}/ptest-runner_2.0.py ${D}${bindir}/ptest-runner
}

do_patch[noexec] = "1"
do_configure[noexec] = "1"
do_compile[noexec] = "1"
do_build[noexec] = "1"
