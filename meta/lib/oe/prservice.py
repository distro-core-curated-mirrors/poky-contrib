
def prserv_make_conn(d, check = False):
    import prserv.serv
<<<<<<< HEAD
    host_params = filter(None, (d.getVar("PRSERV_HOST", True) or '').split(':'))
    try:
        conn = None
        conn = prserv.serv.PRServerConnection(host_params[0], int(host_params[1]))
=======
    host = d.getVar("PRSERV_HOST",True)
    port = d.getVar("PRSERV_PORT",True)
    try:
        conn = None
        conn = prserv.serv.PRServerConnection(host,int(port))
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        if check:
            if not conn.ping():
                raise Exception('service not available')
        d.setVar("__PRSERV_CONN",conn)
    except Exception, exc:
<<<<<<< HEAD
        bb.fatal("Connecting to PR service %s:%s failed: %s" % (host_params[0], host_params[1], str(exc)))
=======
        bb.fatal("Connecting to PR service %s:%s failed: %s" % (host, port, str(exc)))
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

    return conn

def prserv_dump_db(d):
<<<<<<< HEAD
    if not d.getVar('PRSERV_HOST', True):
=======
    if d.getVar('USE_PR_SERV', True) != "1":
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        bb.error("Not using network based PR service")
        return None

    conn = d.getVar("__PRSERV_CONN", True)
    if conn is None:
        conn = prserv_make_conn(d)
        if conn is None:
            bb.error("Making connection failed to remote PR service")
            return None

    #dump db
    opt_version = d.getVar('PRSERV_DUMPOPT_VERSION', True)
    opt_pkgarch = d.getVar('PRSERV_DUMPOPT_PKGARCH', True)
    opt_checksum = d.getVar('PRSERV_DUMPOPT_CHECKSUM', True)
    opt_col = ("1" == d.getVar('PRSERV_DUMPOPT_COL', True))
    return conn.export(opt_version, opt_pkgarch, opt_checksum, opt_col)

def prserv_import_db(d, filter_version=None, filter_pkgarch=None, filter_checksum=None):
<<<<<<< HEAD
    if not d.getVar('PRSERV_HOST', True):
=======
    if d.getVar('USE_PR_SERV', True) != "1":
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        bb.error("Not using network based PR service")
        return None

    conn = d.getVar("__PRSERV_CONN", True)
    if conn is None:
        conn = prserv_make_conn(d)
        if conn is None:
            bb.error("Making connection failed to remote PR service")
            return None
    #get the entry values
    imported = []
    prefix = "PRAUTO$"
    for v in d.keys():
        if v.startswith(prefix):
            (remain, sep, checksum) = v.rpartition('$')
            (remain, sep, pkgarch) = remain.rpartition('$')
            (remain, sep, version) = remain.rpartition('$')
            if (remain + '$' != prefix) or \
               (filter_version and filter_version != version) or \
               (filter_pkgarch and filter_pkgarch != pkgarch) or \
               (filter_checksum and filter_checksum != checksum):
               continue
            try:
                value = int(d.getVar(remain + '$' + version + '$' + pkgarch + '$' + checksum, True))
            except BaseException as exc:
                bb.debug("Not valid value of %s:%s" % (v,str(exc)))
                continue
            ret = conn.importone(version,pkgarch,checksum,value)
            if ret != value:
                bb.error("importing(%s,%s,%s,%d) failed. DB may have larger value %d" % (version,pkgarch,checksum,value,ret))
            else:
               imported.append((version,pkgarch,checksum,value))
    return imported

def prserv_export_tofile(d, metainfo, datainfo, lockdown, nomax=False):
    import bb.utils
    #initilize the output file
    bb.utils.mkdirhier(d.getVar('PRSERV_DUMPDIR', True))
    df = d.getVar('PRSERV_DUMPFILE', True)
    #write data
    lf = bb.utils.lockfile("%s.lock" % df)
    f = open(df, "a")
    if metainfo:
        #dump column info 
        f.write("#PR_core_ver = \"%s\"\n\n" % metainfo['core_ver']);
        f.write("#Table: %s\n" % metainfo['tbl_name'])
        f.write("#Columns:\n")
        f.write("#name      \t type    \t notn    \t dflt    \t pk\n")
        f.write("#----------\t --------\t --------\t --------\t ----\n")
        for i in range(len(metainfo['col_info'])):
            f.write("#%10s\t %8s\t %8s\t %8s\t %4s\n" % 
                    (metainfo['col_info'][i]['name'], 
                     metainfo['col_info'][i]['type'], 
                     metainfo['col_info'][i]['notnull'], 
                     metainfo['col_info'][i]['dflt_value'], 
                     metainfo['col_info'][i]['pk']))
        f.write("\n")

    if lockdown:
        f.write("PRSERV_LOCKDOWN = \"1\"\n\n")

    if datainfo:
        idx = {}
        for i in range(len(datainfo)):
            pkgarch = datainfo[i]['pkgarch']
            value = datainfo[i]['value']
<<<<<<< HEAD
            if pkgarch not in idx:
=======
            if not idx.has_key(pkgarch):
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
                idx[pkgarch] = i
            elif value > datainfo[idx[pkgarch]]['value']:
                idx[pkgarch] = i
            f.write("PRAUTO$%s$%s$%s = \"%s\"\n" % 
                (str(datainfo[i]['version']), pkgarch, str(datainfo[i]['checksum']), str(value)))
        if not nomax:
            for i in idx:
                f.write("PRAUTO_%s_%s = \"%s\"\n" % (str(datainfo[idx[i]]['version']),str(datainfo[idx[i]]['pkgarch']),str(datainfo[idx[i]]['value'])))
    f.close()
    bb.utils.unlockfile(lf)

def prserv_check_avail(d):
<<<<<<< HEAD
    host_params = filter(None, (d.getVar("PRSERV_HOST", True) or '').split(':'))
    try:
        if len(host_params) != 2:
            raise TypeError
        else:
            int(host_params[1])
    except TypeError:
        bb.fatal('Undefined/incorrect PRSERV_HOST value. Format: "host:port"')
=======
    host = d.getVar("PRSERV_HOST",True)
    port = d.getVar("PRSERV_PORT",True)
    try:
        if not host:
            raise TypeError
        else:
            port = int(port)
    except TypeError:
        bb.fatal("Undefined or incorrect values of PRSERV_HOST or PRSERV_PORT")
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
    else:
        prserv_make_conn(d, True)
