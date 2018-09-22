def raise_sanity_error(msg, d, network_error=False):
    if d.getVar("SANITY_USE_EVENTS") == "1":
        try:
            bb.event.fire(bb.event.SanityCheckFailed(msg, network_error), d)
        except TypeError:
            bb.event.fire(bb.event.SanityCheckFailed(msg), d)
        return

    bb.fatal(""" OE-core's config sanity checker detected a potential misconfiguration.
    Either fix the cause of this error or at your own risk disable the checker (see sanity.conf).
    Following is the list of potential problems / advisories:
    
    %s""" % msg)

def check_sanity(sanity_data):
    try:
        result = subprocess.check_output(['check-xlinx-toolchain'], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise_sanity_error("Couldn't find the xlinx toolchain", sanity_data)

addhandler check_sanity_eventhandler
check_sanity_eventhandler[eventmask] = "bb.event.SanityCheck bb.event.NetworkTest"
python check_sanity_eventhandler() {
    if bb.event.getName(e) == "SanityCheck":
        check_sanity(e.data)
        if e.generateevents:
            sanity_data.setVar("SANITY_USE_EVENTS", "1")
        bb.event.fire(bb.event.SanityCheckPassed(), e.data)
    return
}
