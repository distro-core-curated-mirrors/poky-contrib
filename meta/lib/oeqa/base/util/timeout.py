#!/usr/bin/env python
# Copyright (C) 2013 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

# timeout decorator used by test case
# This provides the timeout mechansim for pyunit TC
# usage: @timeout(seconds)

"""Timeout Module"""
import sys
import signal
from functools import wraps

class TimeOut(BaseException):
    """timeout expection"""
    pass

def timeout(seconds):
    """timeout decorator"""
    def decorator(fn):
        if hasattr(signal, 'alarm'):
            @wraps(fn)
            def wrapped_f(*args, **kw):
                current_frame = sys._getframe()
                def alarm_handler(signal, frame):
                    if frame is not current_frame:
                        raise TimeOut('%s seconds' % seconds)
                prev_handler = signal.signal(signal.SIGALRM, alarm_handler)
                try:
                    signal.alarm(seconds)
                    return fn(*args, **kw)
                finally:
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, prev_handler)
            return wrapped_f
        else:
            return fn
    return decorator
