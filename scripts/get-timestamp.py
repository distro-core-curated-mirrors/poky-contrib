#!/usr/bin/env python
#
# Simple script that gets a timestamp (event_time) field from a patchwork event

import json
import fileinput

def ts(lines, timestamp_field = 'event_time'):
    ts_array = []
    for line in lines:
        try:
            obj = json.loads(line)
            ts_array.append(obj[timestamp_field])
        except:
            pass

    return ts_array            

if __name__ == '__main__':

    for timestamp in ts(fileinput.input('-')):
        print timestamp
