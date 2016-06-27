DEFAULT_PREFERENCE = "-1"

include gstreamer1.0.inc

LIC_FILES_CHKSUM = "file://COPYING;md5=6762ed442b3822387a51c92d928ead0d \
                    file://gst/gst.h;beginline=1;endline=21;md5=e059138481205ee2c6fc1c079c016d0d"

SRC_URI = " \
    git://anongit.freedesktop.org/gstreamer/gstreamer;branch=1.8;name=base \
    git://anongit.freedesktop.org/gstreamer/common;destsuffix=git/common;name=common \
"

PV = "1.8.2+git${SRCPV}"

UPSTREAM_CHECK_GITTAGREGEX = "(?P<pver>(\d+(\.\d+)+))"

SRCREV_base = "3de8a4f728a7194a12b784ec4085f6a8e7d9b5bd"
SRCREV_common = "f363b3205658a38e84fa77f19dee218cd4445275"
SRCREV_FORMAT = "base"

S = "${WORKDIR}/git"

# The option to configure tracer hooks was added prior to the 1.7.2 release
# https://cgit.freedesktop.org/gstreamer/gstreamer/commit/?id=e5ca47236e4df4683707f0bcf99181a937d358d5
PACKAGECONFIG[gst-tracer-hooks] = "--enable-gst-tracer-hooks,--disable-gst-tracer-hooks,"
PACKAGECONFIG[trace-historic] = "--enable-trace,--disable-trace,"

do_configure_prepend() {
	${S}/autogen.sh --noconfigure
}
