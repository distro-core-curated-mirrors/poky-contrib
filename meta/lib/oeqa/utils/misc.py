# Copyright (C) 2013-2017 Intel Corporation
#
# Released under the MIT license (see COPYING.MIT)

def getline(data, line):
    _line = ''
    for l in data.split('\n'):
        if line in l:
            _line = l
            break
    return _line
