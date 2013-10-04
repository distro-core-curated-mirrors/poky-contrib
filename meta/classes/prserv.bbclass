def prserv_get_pr_auto(d):
    import oe.prservice
<<<<<<< HEAD
    import re

    pv = d.getVar("PV", True)
    if not d.getVar('PRSERV_HOST', True):
        if 'AUTOINC' in pv:
            d.setVar("PKGV", pv.replace("AUTOINC", "0"))
=======
    if d.getVar('USE_PR_SERV', True) != "1":
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        bb.warn("Not using network based PR service")
        return None

    version = d.getVar("PRAUTOINX", True)
    pkgarch = d.getVar("PACKAGE_ARCH", True)
    checksum = d.getVar("BB_TASKHASH", True)

<<<<<<< HEAD
    conn = d.getVar("__PRSERV_CONN", True)
    if conn is None:
        conn = oe.prservice.prserv_make_conn(d)
        if conn is None:
            return None

    if "AUTOINC" in pv:
        srcpv = bb.fetch2.get_srcrev(d)
        base_ver = "AUTOINC-%s" % version[:version.find(srcpv)]
        value = conn.getPR(base_ver, pkgarch, srcpv)
        d.setVar("PKGV", pv.replace("AUTOINC", str(value)))

    if d.getVar('PRSERV_LOCKDOWN', True):
        auto_rev = d.getVar('PRAUTO_' + version + '_' + pkgarch, True) or d.getVar('PRAUTO_' + version, True) or None
    else:
=======
    if d.getVar('PRSERV_LOCKDOWN', True):
        auto_rev = d.getVar('PRAUTO_' + version + '_' + pkgarch, True) or d.getVar('PRAUTO_' + version, True) or None
    else:
        conn = d.getVar("__PRSERV_CONN", True)
        if conn is None:
            conn = oe.prservice.prserv_make_conn(d)
            if conn is None:
                return None
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        auto_rev = conn.getPR(version, pkgarch, checksum)

    return auto_rev
