# Minimal/stub implementation of the XDG Base Directory specification.
# http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
#
# Wayland needs XDG_RUNTIME_DIR, so it hasn't been set already (by systemd,
# elogind, pam) then create a directory in TMPDIR.

if [ -z "$XDG_RUNTIME_DIR" ]; then
    XDG_RUNTIME_DIR=${TMPDIR:-/tmp}/runtime-${USER}
    mkdir -p ${XDG_RUNTIME_DIR}
    chmod 0700 ${XDG_RUNTIME_DIR}
    export XDG_RUNTIME_DIR
fi
