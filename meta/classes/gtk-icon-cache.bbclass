FILES_${PN} += "${datadir}/icons/hicolor"
<<<<<<< HEAD
=======

DEPENDS += "${@['hicolor-icon-theme', '']['${BPN}' == 'hicolor-icon-theme']}"
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc

DEPENDS += "${@['hicolor-icon-theme', '']['${BPN}' == 'hicolor-icon-theme']} gtk-update-icon-cache-native"

gtk_icon_cache_postinst() {
if [ "x$D" != "x" ]; then
	$INTERCEPT_DIR/postinst_intercept update_icon_cache ${PKG} mlprefix=${MLPREFIX} libdir=${libdir} \
		base_libdir=${base_libdir}
else

	# Update the pixbuf loaders in case they haven't been registered yet
	GDK_PIXBUF_MODULEDIR=${libdir}/gdk-pixbuf-2.0/2.10.0/loaders gdk-pixbuf-query-loaders --update-cache

<<<<<<< HEAD
	for icondir in /usr/share/icons/* ; do
		if [ -d $icondir ] ; then
			gtk-update-icon-cache -fqt  $icondir
		fi
	done
fi
=======
for icondir in /usr/share/icons/* ; do
    if [ -d $icondir ] ; then
        gtk-update-icon-cache -fqt  $icondir
    fi
done
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
}

gtk_icon_cache_postrm() {
if [ "x$D" != "x" ]; then
	$INTERCEPT_DIR/postinst_intercept update_icon_cache ${PKG} mlprefix=${MLPREFIX} libdir=${libdir} \
		base_libdir=${base_libdir}
else
	for icondir in /usr/share/icons/* ; do
		if [ -d $icondir ] ; then
			gtk-update-icon-cache -qt  $icondir
		fi
	done
fi
}

python populate_packages_append () {
    packages = d.getVar('PACKAGES', True).split()
    pkgdest =  d.getVar('PKGDEST', True)
    
    for pkg in packages:
        icon_dir = '%s/%s/%s/icons' % (pkgdest, pkg, d.getVar('datadir', True))
        if not os.path.exists(icon_dir):
            continue

        bb.note("adding hicolor-icon-theme dependency to %s" % pkg)
<<<<<<< HEAD
        rdepends = ' ' + d.getVar('MLPREFIX') + "hicolor-icon-theme"
        d.appendVar('RDEPENDS_%s' % pkg, rdepends)
    
        bb.note("adding gtk-icon-cache postinst and postrm scripts to %s" % pkg)
        
        postinst = d.getVar('pkg_postinst_%s' % pkg, True)
=======
        rdepends = d.getVar('RDEPENDS_%s' % pkg, True)
        rdepends = rdepends + ' ' + d.getVar('MLPREFIX') + "hicolor-icon-theme"
        d.setVar('RDEPENDS_%s' % pkg, rdepends)
    
        bb.note("adding gtk-icon-cache postinst and postrm scripts to %s" % pkg)
        
        postinst = d.getVar('pkg_postinst_%s' % pkg, True) or d.getVar('pkg_postinst', True)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        if not postinst:
            postinst = '#!/bin/sh\n'
        postinst += d.getVar('gtk_icon_cache_postinst', True)
        d.setVar('pkg_postinst_%s' % pkg, postinst)

<<<<<<< HEAD
        postrm = d.getVar('pkg_postrm_%s' % pkg, True)
=======
        postrm = d.getVar('pkg_postrm_%s' % pkg, True) or d.getVar('pkg_postrm', True)
>>>>>>> cb9658cf8ab6cf009030dcadde9dc6c54b72bddc
        if not postrm:
            postrm = '#!/bin/sh\n'
        postrm += d.getVar('gtk_icon_cache_postrm', True)
        d.setVar('pkg_postrm_%s' % pkg, postrm)
}

