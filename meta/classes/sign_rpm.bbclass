# Class for generating signed RPM packages.
#
# Configuration variables used by this class:
# RPM_GPG_PASSPHRASE
#           The passphrase of the signing key.
# RPM_GPG_NAME
#           Name of the key to sign with. May be key id or key name.
# RPM_GPG_BACKEND
#           Optional variable for specifying the backend to use for signing.
#           Currently the only available option is 'local', i.e. local signing
#           on the build host.
# GPG_BIN
#           Optional variable for specifying the gpg binary/wrapper to use for
#           signing.
# GPG_PATH
#           Optional variable for specifying the gnupg "home" directory:
#
inherit sanity

RPM_SIGN_PACKAGES='1'
RPM_GPG_BACKEND ?= 'local'


python () {
    if d.getVar('RPM_GPG_PASSPHRASE_FILE'):
        raise_sanity_error('RPM_GPG_PASSPHRASE_FILE is replaced by RPM_GPG_PASSPHRASE', d)
    # Check configuration
    for var in ('RPM_GPG_NAME', 'RPM_GPG_PASSPHRASE'):
        if not d.getVar(var):
            raise_sanity_error("You need to define %s in the config" % var, d)
}

python sign_rpm () {
    import glob
    from oe.gpg_sign import get_signer

    signer = get_signer(d, d.getVar('RPM_GPG_BACKEND'))
    rpms = glob.glob(d.getVar('RPM_PKGWRITEDIR') + '/*')

    signer.sign_rpms(rpms,
                     d.getVar('RPM_GPG_NAME'),
                     d.getVar('RPM_GPG_PASSPHRASE'))
}

do_package_index[depends] += "signing-keys:do_deploy"
do_rootfs[depends] += "signing-keys:do_populate_sysroot"

# Newer versions of gpg (at least 2.1.5 and 2.2.1) have issues when signing occurs in parallel
# so unfortunately the signing must be done serially. Once the upstream problem is fixed,
# the following line must be removed otherwise we loose all the intrinsic parallelism from
# bitbake.  For more information, check https://bugzilla.yoctoproject.org/show_bug.cgi?id=12022.
do_package_write_rpm[lockfiles] += "${TMPDIR}/gpg.lock"
