QAPATHTEST[selftest-walk] = "package_qa_check_selftest_walk"
def package_qa_check_selftest_walk(path, pkg, d, elf, messages):
    path = package_qa_clean_path(path, d, pkg)
    bb.warn("WALK %s %s %s" % (pkg, path, "ELF" if elf else "FILE"))
