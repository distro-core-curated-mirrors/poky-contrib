# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# BitBake Test for lib/bb/persist_data/
#
# Copyright (C) 2018 Garmin International
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
"""
Python wrappers for os.fork() that allow the insertion of callbacks for fork events.
This is designed to exacmimic os.register_at_fork() available in Python 3.7 with the
intent that it can be removed when that version becomes standard
"""

import sys
import os

before_calls = []
after_in_parent_calls = []
after_in_child_calls = []

def _do_calls(l, reverse=False):
    # Make a copy in case the list is modified in the callback
    copy = l[:]
    if reverse:
        copy = reversed(copy)

    for f in copy:
        # All exception in calls are ignored
        try:
            f()
        except:
            pass

def fork():
    if sys.hexversion >= 0x030700F0:
        return os.fork()

    _do_calls(before_calls, reverse=True)

    ret = os.fork()
    if ret == 0:
        _do_calls(after_in_child_calls)
    else:
        _do_calls(after_in_parent_calls)
    return ret

def register_at_fork(*, before=None, after_in_parent=None, after_in_child=None):
    if sys.hexversion >= 0x030700F0:
        os.register_at_fork(before=before, after_in_parent=after_in_parent, after_in_child=after_in_child)
        return

    if before is not None:
        before_calls.append(before)

    if after_in_parent is not None:
        after_in_parent_calls.append(after_in_parent)

    if after_in_child is not None:
        after_in_child_calls.append(after_in_child)

