SUMMARY = "dummy GL"
LICENSE = "MIT"

inherit allarch

RPROVIDES:${PN} = "virtual-libegl-icd virtual-libglx-icd"

ALLOW_EMPTY:${PN} = "1"

BBCLASSEXTEND = "native nativesdk"

DEFAULT_PREFERENCE = "-1"
