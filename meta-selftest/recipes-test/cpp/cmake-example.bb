#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: MIT
#

SUMMARY = "A C++ example compiled with cmake."

require cpp-example.inc

SRC_URI += "file://CMakeLists.txt"

inherit cmake-qemu

PACKAGECONFIG[failing_test] = "-DFAILING_TEST=ON"

FILES:${PN}-ptest += "${bindir}/test-cmake-example"

do_compile_native() {
    export CPPFLAGS=--invalid-cppflags
    export CFLAGS=--invalid-cflags
    export CXXFLAGS=--invalid-cxxflags
    export LDFLAGS=--invalid-ldflags

    rm -rf ${B}/NATIVE
    cmake -S ${S} -B ${B}/NATIVE -DCMAKE_TOOLCHAIN_FILE=${WORKDIR}/toolchain-native.cmake
    cmake --build ${B}/NATIVE
    ${B}/NATIVE/cmake-example
}
addtask do_compile_native after do_configure before do_build

do_run_tests () {
    bbnote ${DESTDIR:+DESTDIR=${DESTDIR} }${CMAKE_VERBOSE} cmake --build '${B}' --target test -- ${EXTRA_OECMAKE_BUILD}
    eval ${DESTDIR:+DESTDIR=${DESTDIR} }${CMAKE_VERBOSE} cmake --build '${B}' --target test -- ${EXTRA_OECMAKE_BUILD}
}
do_run_tests[doc] = "Run cmake --target=test using qemu-user"

addtask do_run_tests after do_compile

BBCLASSEXTEND = "nativesdk"
