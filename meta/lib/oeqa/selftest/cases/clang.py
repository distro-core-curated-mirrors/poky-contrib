# clang.py — oe-selftest integration with dynamic CHECK_TARGET for clang-testsuite.inc

import os
import time
from datetime import datetime
from oeqa.core.case import OEPTestResultTestCase
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, get_bb_vars, runqemu
from oeqa.core.decorator import OETestTag
from oeqa.utils.commands import get_bb_vars

bb_vars = get_bb_vars(["WORKDIR"], "clang-native")
workdir = bb_vars["WORKDIR"]

logdir = os.path.join(workdir, "temp")
LOGFILE = os.path.join(logdir, "clang.log")

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S,%f")[:-3]
    line = f"[{ts}] {msg}"
    print(line)

    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

class ClangSelfTestBase(OESelftestTestCase, OEPTestResultTestCase):
    def run_check(self, *suites, ssh=None):
        log("Entering run_check() with suites: {}".format(suites))
        
        recipe = "clang"
        start_time = time.time()

        try:
            log(f"Running: bitbake {recipe}-native -c check")
            bitbake(f'{recipe}-native -c check')
        except Exception as e:
            log(f"bitbake failed: {e}")
            raise

        end_time = time.time()
        log(f"bitbake completed in {int(end_time - start_time)} seconds.")

@OETestTag("toolchain-user")
class ClangCheckTest(ClangSelfTestBase):
    def test_check_clang(self):
        log("=== Starting check-clang ===")
        self.run_check("clang")
        log("=== Finished check-clang ===")
