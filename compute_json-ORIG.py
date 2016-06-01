#!/bin/python

import json
from datetime import datetime, timedelta
import numpy as np
import scipy as sp
import scipy.stats
import sys
import os.path
from scipy import stats
from math import sqrt


cols = [
        {
            "type": "string",
            "id": "commits",
            "label": "Commit name"
        },
        {
            "type": "datetime",
            "id": "average",
            "label": "Average time"
        },
        {
            "type": "datetime",
            "id": "i0",
            "role": "interval",
            "label": "Interval1"
        },
        {
            "type": "datetime",
            "id": "i1",
            "role": "interval",
            "label": "Interval2"
	},
{
            "type": "datetime",
            "id": "i2",
            "role": "interval",
            "label": "Point1"
        },
        {
            "type": "datetime",
            "id": "i2",
            "role": "interval",
            "label": "Point2"
        },
        {
            "type": "datetime",
            "id": "i2",
            "role": "interval",
            "label": "Point3"
        },
        {
            "role": "interval",
            "type": "datetime",
            "id": "i2",
            "label": "Point4"
        },
        {
            "role": "interval",
            "type": "datetime",
            "id": "i2",
            "label": "Point5"
        },
        {
            "role": "interval",
            "type": "datetime",
            "id": "i2",
            "label": "Point6"
        },
        {
            "role": "interval",
            "type": "datetime",
            "id": "i2",
            "label": "Point7"
        },
        {
            "role": "interval",
            "type": "datetime",
            "id": "i2",
            "label": "Point8"
        },
        {
            "role": "interval",
            "type": "datetime",
            "id": "i2",
            "label": "Point9"
        }
    ]

#
#Usage
#

if len(sys.argv)!= 3:
	print "./compute_json.py accepts only one argument"
	print "Usage: ./compute_json.py <arg> <input_file>"
	exit(1)
elif type(int(sys.argv[1])) is not int:
	print " Usage: ./copmute_json.py <arg> <input_file>"
	print " where [arg] is int"
	exit (1)
elif not os.path.isfile(sys.argv[2]):
	print "USage: ./compute_json.py <arg> <input_file>"
	exit (1)
	
	
option = int(sys.argv[1])
input = sys.argv[2]

#function check if line creates new column or adds to existing column

def check_col(rows, items):
	commit = items[2]
#	values = items[8].split(":")
# the items column is passed as a python script argument sys.argv[1]
	timed   = items[int(option)].split(".")
	val = timed[0].split(":")
	if len(val) == 2:
		val.insert(0,"0")

	values = val
#	print "values", values

	build_time = timedelta(hours=int(values[0]), minutes=int(values[1]), seconds=int(values[2]))
	for row in rows:
		current_commit = row["c"][0]["v"]
		
		if current_commit == commit:
			row["sum"] += build_time
			row["runs"] += 1
			row["build_times"].append(build_time.total_seconds())
			date_obj = datetime.now()
			date_obj = date_obj.replace(hour=int(values[0]), minute=int(values[1]), second=int(values[2]))
			fmt = "Date(%Y,%m,%d,%H,%M,%S,0)"
			row["c"].append({"f": "Point{}".format(row["runs"]), "v": date_obj.strftime(fmt)}) 
			return row 
	row = {"c": [{"v": commit}], "sum": timedelta(), "runs": 0, "build_times": []}
	rows.append(row)
	return check_col(rows, items)


rows = []

#with open ("input.csv", "r") as f:
#with open ("input.csv", "r") as f:

with open(input, "r") as f:
	for line in f:
		items = line.split(",")
		commit = items[1]
		check_col(rows, items)

for row in rows:
#compute confidence intervals based on standard deviation
	avg_td = row["sum"] // row["runs"]
	avg = avg_td.total_seconds()

	variance = map(lambda x: (x - avg) ** 2, row["build_times"])
	std_dev = sqrt(sum(variance) / row["runs"])

	se = stats.sem(row["build_times"])
	h = se * stats.t._ppf((1 + 0.95) / 2., row["runs"] - 1)
#	print(row["build_times"] + [std_dev, avg, avg-h, avg+h])

	high_int = avg + h
	low_int = avg -h
#make low_int = 0 if negative
	if low_int < 0: 
		low_int = 0

#	avg, low_int, high_int = mean_confidence_interval(row)
#	low_int, high_int = stats.norm.interval(0.05, loc=avg, scale=std_dev)
#	print(row["build_times"] + [std_dev, avg, low_int, high_int])
#second_attempt std dev


#	mean_confidence_interval(row)

#write average time to JSON	
	hours, remainder = divmod(int(avg), 3600)
	minutes, seconds = divmod(remainder, 60)
	date_obj = datetime.now()
	date_obj = date_obj.replace(hour=hours, minute=minutes, second=seconds)
	fmt = "Date(%Y,%m,%d,%H,%M,%S,0)"
	fmt_print = "%H:%M:%S"
	row["c"].insert(1, {"f": date_obj.strftime(fmt_print), "v": date_obj.strftime(fmt)})

#compute and write top an bottom intervals based on the confidence intervals
	hours, remainder = divmod(int(high_int), 3600)
        minutes, seconds = divmod(remainder, 60)
        date_obj = datetime.now()
        date_obj = date_obj.replace(hour=hours, minute=minutes, second=seconds)	
	row["c"].insert(2, {"f": date_obj.strftime(fmt_print), "v": date_obj.strftime(fmt)})
	
	hours, remainder = divmod(int(low_int), 3600)
        minutes, seconds = divmod(remainder, 60)
        date_obj = datetime.now()
        date_obj = date_obj.replace(hour=hours, minute=minutes, second=seconds)	
	row["c"].insert(3, {"f": date_obj.strftime(fmt_print), "v": date_obj.strftime(fmt)})
	
	del row["sum"]
	del row["runs"]
	del row["build_times"]
#	break
print(json.dumps({"rows": rows, "cols": cols}))
