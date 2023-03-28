SUMMARY = "WebKit web rendering engine for the GTK+ platform"
HOMEPAGE = "https://www.webkitgtk.org/"
BUGTRACKER = "https://bugs.webkit.org/"

LICENSE = "BSD-2-Clause & LGPL-2.0-or-later"
LIC_FILES_CHKSUM = "file://Source/JavaScriptCore/COPYING.LIB;md5=d0c6d6397a5d84286dda758da57bd691 \
                    file://Source/WebCore/LICENSE-APPLE;md5=4646f90082c40bcf298c285f8bab0b12 \
                    file://Source/WebCore/LICENSE-LGPL-2;md5=36357ffde2b64ae177b2494445b79d21 \
                    file://Source/WebCore/LICENSE-LGPL-2.1;md5=a778a33ef338abbaf8b8a7c36b6eec80 \
                    "

SRC_URI = "https://www.webkitgtk.org/releases/${BPN}-${PV}.tar.xz \
           file://0001-FindGObjectIntrospection.cmake-prefix-variables-obta.patch \
           file://0001-FindLibGcrypt.cmake-check-PC_GCRYPT_FOUND.patch \
           file://reproducibility.patch \
           file://0d3344e17d258106617b0e6d783d073b188a2548.patch \
           file://disable_wasm_riscv64.patch \
           file://0001-ANGLE-Remove-static_assert-for-64bit-atomics.patch \
           "
SRC_URI[sha256sum] = "a4607ea1bf89669e89b1cb2c63faaec513f93de09b6ae60cc71d6a8aab7ab393"

inherit cmake ccache pkgconfig gobject-introspection perlnative features_check upstream-version-is-even gi-docgen mime-xdg

ANY_OF_DISTRO_FEATURES = "${GTK3DISTROFEATURES}"
REQUIRED_DISTRO_FEATURES = "opengl"

CVE_PRODUCT = "webkitgtk webkitgtk\+"

DEPENDS += " \
          atk \
          cairo \
          gperf-native \
          gstreamer1.0 \
          gstreamer1.0-plugins-base \
          glib-2.0-native \
          gettext-native \
          gstreamer1.0-plugins-bad \
          ${@bb.utils.contains('LICENSE_FLAGS', 'commercial', 'gstreamer1.0-libav', '', d)} \
          harfbuzz \
          jpeg \
          libnotify \
          libsoup \
          libtasn1 \
          libwebp \
          libxslt \
          ruby-native \
          unifdef-native \
          "

PACKAGECONFIG ??= "${@bb.utils.filter('DISTRO_FEATURES', 'wayland x11 opengl', d)} \
                   ${@bb.utils.contains('DISTRO_FEATURES', 'x11 opengl', 'webgl opengl gst-gl', '', d)} \
                   ${@bb.utils.contains('DISTRO_FEATURES', 'wayland opengl', 'webgl gles2 gst-gl', '', d)} \
                   ${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'journald', '', d)} \
                   gtk4 \
                   enchant \
                   libsecret \
                  "

PACKAGECONFIG[wayland] = "-DENABLE_WAYLAND_TARGET=ON,-DENABLE_WAYLAND_TARGET=OFF,wayland wayland-native libwpe wpebackend-fdo"
PACKAGECONFIG[angle] = "-DUSE_ANGLE_EGL=ON,-DUSE_ANGLE_EGL=OFF,virtual/egl"
PACKAGECONFIG[bubblewrap] = "-DENABLE_BUBBLEWRAP_SANDBOX=ON,-DENABLE_BUBBLEWRAP_SANDBOX=OFF,bubblewrap-native libseccomp xdg-dbus-proxy-native,bubblewrap xdg-dbus-proxy"
PACKAGECONFIG[x11] = "-DENABLE_X11_TARGET=ON,-DENABLE_X11_TARGET=OFF,virtual/libx11 libxcomposite libxdamage libxrender libxt"
PACKAGECONFIG[libavif] = "-DUSE_AVIF=ON,-DUSE_AVIF=OFF,libavif"
PACKAGECONFIG[gtk4] = "-DUSE_GTK4=ON,-DUSE_GTK4=OFF,gtk4"
PACKAGECONFIG[gamepad] = "-DENABLE_GAMEPAD=ON,-DENABLE_GAMEPAD=OFF,libmanette"
PACKAGECONFIG[geoclue] = "-DENABLE_GEOLOCATION=ON,-DENABLE_GEOLOCATION=OFF,geoclue"
PACKAGECONFIG[enchant] = "-DENABLE_SPELLCHECK=ON,-DENABLE_SPELLCHECK=OFF,enchant2"
PACKAGECONFIG[gles2] = "-DENABLE_GLES2=ON,-DENABLE_GLES2=OFF,virtual/libgles2"
PACKAGECONFIG[webgl] = "-DENABLE_WEBGL=ON,-DENABLE_WEBGL=OFF,virtual/egl"
PACKAGECONFIG[opengl] = "-DUSE_OPENGL_OR_ES=ON,-DUSE_OPENGL_OR_ES=OFF,virtual/egl libepoxy"
PACKAGECONFIG[libsecret] = "-DUSE_LIBSECRET=ON,-DUSE_LIBSECRET=OFF,libsecret"
PACKAGECONFIG[libhyphen] = "-DUSE_LIBHYPHEN=ON,-DUSE_LIBHYPHEN=OFF,libhyphen"
PACKAGECONFIG[webrtc] = "-DENABLE_WEB_RTC=ON -DUSE_GSTREAMER_WEBRTC=ON,-DENABLE_WEB_RTC=OFF"
PACKAGECONFIG[woff2] = "-DUSE_WOFF2=ON,-DUSE_WOFF2=OFF,woff2"
PACKAGECONFIG[openjpeg] = "-DUSE_OPENJPEG=ON,-DUSE_OPENJPEG=OFF,openjpeg"
PACKAGECONFIG[reduce-size] = "-DCMAKE_BUILD_TYPE=MinSizeRel,-DCMAKE_BUILD_TYPE=Release,,"
PACKAGECONFIG[lcms] = "-DUSE_LCMS=ON,-DUSE_LCMS=OFF,lcms"
PACKAGECONFIG[journald] = "-DENABLE_JOURNALD_LOG=ON,-DENABLE_JOURNALD_LOG=OFF,systemd"
PACKAGECONFIG[gst-gl] ="-DUSE_GSTREAMER_GL=ON,-DUSE_GSTREAMER_GL=OFF"
PACKAGECONFIG[gst-transcoder] ="-DUSE_GSTREAMER_TRANSCODER=ON,-DUSE_GSTREAMER_TRANSCODER=OFF,gstreamer1.0-plugins-bad"

EXTRA_OECMAKE = " \
		-DENABLE_2022_GLIB_API=ON \
		-DPORT=GTK \
		-DUSE_XDGMIME=ON \
		-DBWRAP_EXECUTABLE=${bindir}/bwrap \
		-DDBUS_PROXY_EXECUTABLE=${bindir}/xdg-dbus-proxy \
		${@bb.utils.contains('GI_DATA_ENABLED', 'True', '-DENABLE_INTROSPECTION=ON', '-DENABLE_INTROSPECTION=OFF', d)} \
		${@bb.utils.contains('GIDOCGEN_ENABLED', 'True', '-DENABLE_DOCUMENTATION=ON', '-DENABLE_DOCUMENTATION=OFF', d)} \
		-DENABLE_MINIBROWSER=ON \
                "

# Javascript JIT is not supported on ARC
EXTRA_OECMAKE:append:arc = " -DENABLE_JIT=OFF "
# By default 25-bit "medium" calls are used on ARC
# which is not enough for binaries larger than 32 MiB
CFLAGS:append:arc = " -mlong-calls"
CXXFLAGS:append:arc = " -mlong-calls"

# Needed for non-mesa graphics stacks when x11 is disabled
CXXFLAGS += "${@bb.utils.contains('DISTRO_FEATURES', 'x11', '', '-DEGL_NO_X11=1', d)}"

# Javascript JIT is not supported on powerpc
EXTRA_OECMAKE:append:powerpc = " -DENABLE_JIT=OFF "
EXTRA_OECMAKE:append:powerpc64 = " -DENABLE_JIT=OFF "

# ARM JIT code does not build on ARMv4/5/6 anymore
EXTRA_OECMAKE:append:armv5 = " -DENABLE_JIT=OFF "
EXTRA_OECMAKE:append:armv6 = " -DENABLE_JIT=OFF "
EXTRA_OECMAKE:append:armv4 = " -DENABLE_JIT=OFF "

EXTRA_OECMAKE:append:mipsarch = " -DUSE_LD_GOLD=OFF "
EXTRA_OECMAKE:append:powerpc = " -DUSE_LD_GOLD=OFF "

# JIT and WASM does not work on RISCV
EXTRA_OECMAKE:append:riscv32 = " -DENABLE_JIT=OFF -DENABLE_WEBASSEMBLY=OFF"
EXTRA_OECMAKE:append:riscv64 = " -DENABLE_JIT=OFF -DENABLE_WEBASSEMBLY=OFF"

# JIT not supported on MIPS either
EXTRA_OECMAKE:append:mipsarch = " -DENABLE_JIT=OFF -DENABLE_C_LOOP=ON "

# JIT not supported on X32
# An attempt was made to upstream JIT support for x32 in
# https://bugs.webkit.org/show_bug.cgi?id=100450, but this was closed as
# unresolved due to limited X32 adoption.
EXTRA_OECMAKE:append:x86-x32 = " -DENABLE_JIT=OFF "

SECURITY_CFLAGS:remove:aarch64 = "-fpie"
SECURITY_CFLAGS:append:aarch64 = " -fPIE"

FILES:${PN} += "${libdir}/webkitgtk-6.*/injected-bundle"

RRECOMMENDS:${PN} += "ca-certificates shared-mime-info"

# http://errors.yoctoproject.org/Errors/Details/20370/
ARM_INSTRUCTION_SET:armv4 = "arm"
ARM_INSTRUCTION_SET:armv5 = "arm"
ARM_INSTRUCTION_SET:armv6 = "arm"

# https://bugzilla.yoctoproject.org/show_bug.cgi?id=9474
# https://bugs.webkit.org/show_bug.cgi?id=159880
# JSC JIT can build on ARMv7 with -marm, but doesn't work on runtime.
# Upstream only tests regularly the JSC JIT on ARMv7 with Thumb2 (-mthumb).
ARM_INSTRUCTION_SET:armv7a = "thumb"
ARM_INSTRUCTION_SET:armv7r = "thumb"
ARM_INSTRUCTION_SET:armv7ve = "thumb"

# introspection inside qemu-arm hangs forever on musl/arm builds
# therefore disable GI_DATA
GI_DATA_ENABLED:libc-musl:armv7a = "False"
GI_DATA_ENABLED:libc-musl:armv7ve = "False"

PACKAGE_PREPROCESS_FUNCS += "src_package_preprocess"
src_package_preprocess () {
        # Trim build paths from comments in generated sources to ensure reproducibility
        sed -i -e "s,${WORKDIR},,g" \
            ${B}/JavaScriptCore/DerivedSources/*.h \
            ${B}/JavaScriptCore/DerivedSources/yarr/*.h \
            ${B}/JavaScriptCore/PrivateHeaders/JavaScriptCore/*.h \
            ${B}/WebKitGTK/DerivedSources/webkit/*.cpp \
            ${B}/WebKitGTK/DerivedSources/webkit/*.h
}
