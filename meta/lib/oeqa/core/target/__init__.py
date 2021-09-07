#
# Copyright (C) 2016 Intel Corporation
#
# SPDX-License-Identifier: MIT
#


class OETarget:

    def __init__(self, logger, server_ip):
        self.server_ip = server_ip
        self.logger = logger

    def start(self):
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
