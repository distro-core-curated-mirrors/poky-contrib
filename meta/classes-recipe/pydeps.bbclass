PACKAGEFUNCS:prepend = "gen_pydeps"
python gen_pydeps() {
    # TODO until we bump our minimum Py dependency to 3.11 I think
    # we should ship tomli/tomllib as oe.tomllib.
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    # TODO can we assume these? Don't think so
    import packaging.markers
    import packaging.requirements

    with open(d.expand("${S}/pyproject.toml"), "rb") as f:
        metadata = tomllib.load(f)

    rdepends = d.expand("RDEPENDS:${PN}")

    # TODO This is the build host environment, not the target environment.
    # Using the siteconfig trick should make this work, or generate our own by hand:
    # {'implementation_name': 'cpython', 'implementation_version': '3.10.12', 'os_name': 'posix', 'platform_machine': 'aarch64', 'platform_release': '6.5.0-27-generic', 'platform_system': 'Linux', 'platform_version': '#28~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Mar 15 15:33:03 UTC 2', 'python_full_version': '3.10.12', 'platform_python_implementation': 'CPython', 'python_version': '3.10', 'sys_platform': 'linux'}
    env = packaging.markers.default_environment()
    env["python_version"] = "3.12"

    reqs = [packaging.requirements.Requirement(req) for req in metadata['project']['dependencies']]
    for req in (r for r in reqs if not r.marker or r.marker.evaluate(env)):
        # TODO specifier will need to transformed
        ver = req.specifier and f" ({req.specifier})" or ""
        # TODO seems like opkg doesn't like versioned provides? test with RPM but for now don't set version
        ver = ""
        d.appendVar(rdepends, f" python-module-{req.name}{ver}")
}

# TODO to silence ERROR: QA Issue: python3-jsonschema rdepends on python-module(jsonschema-specifications), but it isn't a build dependency? [build-deps]
# most likely need to rdepend in the future
INSANE_SKIP:${PN} += "build-deps"
