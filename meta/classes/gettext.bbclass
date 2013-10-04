def gettext_dependencies(d):
<<<<<<< HEAD
    if d.getVar('INHIBIT_DEFAULT_DEPS', True) and not oe.utils.inherits(d, 'cross-canadian'):
        return ""
    if d.getVar('USE_NLS', True) == 'no':
=======
    if d.getVar('USE_NLS', True) == 'no' and not oe.utils.inherits(d, 'native', 'nativesdk', 'cross'):
        return ""
    if d.getVar('INHIBIT_DEFAULT_DEPS', True) and not oe.utils.inherits(d, 'cross-canadian'):
        return ""
    if oe.utils.inherits(d, 'native', 'cross'):
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        return "gettext-minimal-native"
    return d.getVar('DEPENDS_GETTEXT', False)

def gettext_oeconf(d):
<<<<<<< HEAD
    if d.getVar('USE_NLS', True) == 'no':
        return '--disable-nls'
    # Remove the NLS bits if USE_NLS is no or INHIBIT_DEFAULT_DEPS is set
    if d.getVar('INHIBIT_DEFAULT_DEPS', True) and not oe.utils.inherits(d, 'cross-canadian'):
=======
    if oe.utils.inherits(d, 'native', 'cross'):
        return '--disable-nls'
    # Remove the NLS bits if USE_NLS is no.
    if d.getVar('USE_NLS', True) == 'no' and not oe.utils.inherits(d, 'nativesdk', 'cross-canadian'):
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        return '--disable-nls'
    return "--enable-nls"

DEPENDS_GETTEXT ??= "virtual/gettext gettext-native"

BASEDEPENDS =+ "${@gettext_dependencies(d)}"
EXTRA_OECONF_append = " ${@gettext_oeconf(d)}"
