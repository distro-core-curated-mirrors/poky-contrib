#!/bin/python
import sys
import os.path

#
#Usage
#

if len(sys.argv)!= 3:
	print "./clean-csv.py accepts only one argument:"
	print "Usage: ./clean-csv.py <input_file> <output_file>"
	exit(1)
elif not os.path.isfile(sys.argv[1]):
	print "No input_file found!"
	print "Usage: ./compute_json.py <input_file> <output_file>"
	exit (1)
	
input = sys.argv[1]
output_file = sys.argv[2]

TEST_BRANCH = "master"

#returns if row_branch equals with TEST_BRANCH
def check_branch(input_row, branch):
	temp = input_row.split(",")
	if len(temp) != 12:
		return False
	else:
		temp = temp[1]
		current_branch = temp.split(":")
		current_branch = current_branch[0]

	if (current_branch == branch):
		return True
	else:
		return False

#returns the no of commits in the file same as one in current_row
def check_no_commits(input_rows, current_row):
	commit_no = 0
	current_row_commit = current_row.split(",")[1]
	current_row_commit = current_row_commit.split(":")[1]

	for row in input_rows:
		items = row.split(",")
		tmp = items[1]
		tmp = tmp.split(":")
		current_commit = tmp[1]

		if current_commit == current_row_commit:
			commit_no += 1
	return commit_no

#checks if fields are null or \n in the CSV
def check_null_times(current_row):
	row_elements = current_row.split(",")

#	print row_elements
	for element in row_elements:
		if element == "" or element == "\n" or element == "0":
#			print "false"
			return False
			break
	return True

#reading the csv file
input_rows = []
with open(input, "r") as f:
	for line in f:
		if check_branch(line,TEST_BRANCH) and check_null_times(line):
			input_rows.append(line)

#writing the new cleaned csv file
with open(output_file, "w") as f:
	for line in input_rows:
		if check_no_commits(input_rows,line) > 2:
			# print line
		 	f.write(line)