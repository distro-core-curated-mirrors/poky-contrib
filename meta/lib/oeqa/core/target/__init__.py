#
# Copyright (C) 2016 Intel Corporation
#
# SPDX-License-Identifier: MIT
#


class OETarget:
    """
    Interface between the host system and the test target, used by the runtime
    test suite (testimage).
    """

    def __init__(self, logger, target_ip, server_ip):
        self.ip = target_ip
        self.server_ip = server_ip
        self.logger = logger

    def start(self):
        """
        Start the target if required, raising an exception on error.
        """
        pass

    def stop(self):
        pass

    def run(self, cmd, timeout=None):
        pass

    def copyTo(self, localSrc, remoteDst):
        pass

    def copyFrom(self, remoteSrc, localDst):
        pass

    def copyDirTo(self, localSrc, remoteDst):
        pass
