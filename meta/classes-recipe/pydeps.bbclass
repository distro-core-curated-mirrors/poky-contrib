inherit python3-dir

PACKAGEFUNCS += "package_generate_pydeps"

python package_generate_pydeps() {
    import modulefinder
    paths = (
        d.expand("${RECIPE_SYSROOT}${PYTHON_SITEPACKAGES_DIR}"),
        d.expand("${RECIPE_SYSROOT}${libdir}/${PYTHON_DIR}/")
    )
    finder = modulefinder.ModuleFinder(paths)

    for pkg in d.getVar("PACKAGES").split():
        for path in pkgfiles[pkg]:
            if not path.endswith(".py"):
                continue

            bb.plain("Scanning %s" % path)
            finder.load_file(path)
            bb.plain("Modules found: " + " ".join(finder.modules.keys()))   
            bb.plain("Modules not found: " + " ".join(finder.badmodules.keys()))   
}
