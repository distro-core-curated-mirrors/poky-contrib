# A recipe to test the same test cases as the override-cache test cases.
#
# Run with "bitbake -b test.bb -fc test"
LICENSE = "CLOSED"

INHIBIT_DEFAULT_DEPS = "1"

inherit nopackages


VAR = "0"
VAR:b = "1"
VAR:a:b = "5"
VAR:a:c = "4"
VAR:b:d = "3"
VAR:b:a = "2"
VAR:f = "6"

python do_test() {
    def e(varname, overrides=""):
        localdata = bb.data.createCopy(d)
        localdata.setVar("OVERRIDES", overrides)
        ret = localdata.getVar(varname)
        bb.plain(f"{varname} ({overrides}) = {ret}")
        return ret

    # Test cases
    assert e("VAR") == "0"
    assert e("VAR:b") == "1"
    assert e("VAR:a") is None
    assert e("VAR:c") is None
    assert e("VAR:d") is None

    # No override defined for "A"
    assert e("VAR", "a") == "0"
    assert e("VAR", "b") == "1"

    # No directly assigned value for VAR:C; defaults to VAR
    assert e("VAR", "c") == "0"

    # C is higher priority, but has no value defined, so B is used
    assert e("VAR", "b:c") == "1"

    assert e("VAR", "b:f") == "6"
    assert e("VAR", "f:b") == "1"

    # Priority crisscross
    assert e("VAR", "b:a") == "2"
    assert e("VAR", "a:b") == "5"

}

addtask test

