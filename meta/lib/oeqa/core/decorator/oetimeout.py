# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

import signal
from oeqa.core.exception import OEQATimeoutError
from oeqa.core.decorator.base import OETestDecorator, registerDecorator

@registerDecorator
class OETimeout(OETestDecorator):
    attrs = ('oetimeout',)

    def setUpDecorator(self):
        timeout = self.oetimeout
        def _timeoutHandler(signum, frame):
            raise OEQATimeoutError("Timed out after %s "
                    "seconds of execution" % timeout)

        self.logger.debug("Setting up a %d second(s) timeout" % self.oetimeout)
        self.alarmSignal = signal.signal(signal.SIGALRM, _timeoutHandler)
        signal.alarm(self.oetimeout)

    def tearDownDecorator(self):
        signal.alarm(0)
        signal.signal(signal.SIGALRM, self.alarmSignal)
        self.logger.debug("Removed SIGALRM handler")
