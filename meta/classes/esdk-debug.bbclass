addhandler esdk_eventhandler
esdk_eventhandler[eventmask] = "bb.event.SetSceneEnforceFailure"

python esdk_eventhandler() {
    import glob
    for entry in e.failedtasks:
        (mc, fn, taskname, taskfn, pn, setscened, hash) = entry

        present = False
        if setscened:
            sstatepath = '%s/%s/sstate:%s:*:%s_%s.tgz' % (d.getVar('SSTATE_DIR'), hash[:2], pn, hash, taskname)
            if glob.glob(sstatepath):
                present = True
        if setscened:
            bb.warn('%s.%s %s %s' % (pn, taskname, hash, present))
        else:
            bb.warn('%s.%s %s' % (pn, taskname, hash))
}

BB_HASHCONFIG_WHITELIST_append = " esdk_eventhandler"
