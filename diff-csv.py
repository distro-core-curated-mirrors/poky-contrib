#!/bin/python
import sys
import os.path

#
#Usage
#

if len(sys.argv)!= 3:
	print "./clean-csv.py accepts only two arguments as input files:"
	print "Usage: ./clean-csv.py <input_file> <input_file1>"
	exit(1)
elif not os.path.isfile(sys.argv[1]):
	print "No <input_file1> found!"
	print "Usage: ./compute_json.py <input_file1> <input_file1>"
	exit (1)
elif not os.path.isfile(sys.argv[2]):
	print "No <input_file2> found!"
	print "Usage: ./compute_json.py <input_file> <input_file1>"
	exit (1)

#define working files 
file1 = sys.argv[1]
new_file1 = "new_file1.csv"
output1 = "input-ubuntu.csv"
file2 = sys.argv[2]
new_file2 = "new_file2.csv"
output2 = "input-fedora.csv"

# gets the commit from a line 
def commit_from_line(line):
	intems = line.split(',')
	tmp = intems[1]
	tmp = tmp.split(":")
	return tmp[1]

# gets the commit list from a csv
def commit_list_from_csv(input_rows):
	commit_list = []
	for line in input_rows:
		# intems = line.split(',')
		# tmp = intems[1]
		# tmp = tmp.split(":")
		# current_commit = tmp[1]

		current_commit = commit_from_line(line)

		if current_commit not in commit_list:
			commit_list.append(current_commit)
	return commit_list

# makes an intersection between the commit_list1 and commit_list2
def diff_commit_list(commit_list1, commit_list2):
	diff_commits = []
	for commit in commit_list1:
		if commit in commit_list2:
			print commit
			diff_commits.append(commit)
	return diff_commits

def check_machine_host(input_lines_f1, input_lines_f2):
	search1 = input_lines_f1[0]
	search2 = input_lines_f2[0]
	if search1.find("ubuntu") and search2.find("fedora"):
		return [output2, output1]
	elif search1.find("fedora") and search2.find("ubuntu"):
		return [output1, output2]
	else:
		print "Wrong hosts in input csv files"
		exit(1)



#reading the first csv file
input_lines_f1 = []
with open(file1, "r") as f:
	for line in f:
		input_lines_f1.append(line)


#reading the  second csv file
input_lines_f2 = []
with open(file2, "r") as f:
	for line in f:
		input_lines_f2.append(line)


#compute the diff
diff = diff_commit_list(commit_list_from_csv(input_lines_f1), commit_list_from_csv(input_lines_f2))

#assign the correct csv output files Ubuntu vs Fedora
output = check_machine_host(input_lines_f1,input_lines_f2)
print "output"
print output
# some debug prints
# print "diff"
# print diff

# print "f1"
# print commit_list_from_csv(input_lines_f1)
# print "f2"
# print commit_list_from_csv(input_lines_f2)


# for line in input_lines_f1:
# 	print line

with open(output[0], "w") as f:
	for line in input_lines_f1:
		# for commit in commit_list_from_csv(input_lines_f1):
			if commit_from_line(line) in diff:
				# print line
				f.write(line)

with open(output[1], "w") as f:
	for line in input_lines_f2:
		# for commit in commit_list_from_csv(input_lines_f2):
			if commit_from_line(line) in diff:
				# print line
				f.write(line)

# print "f1"
# print commit_list_from_csv(input_lines_f1)


# print "f2"
# print commit_list_from_csv(input_lines_f2)
# print "f1"
# for line in input_lines_f1:
# 	print commit_list_from_csv(line)

# print "f2"
# for line in input_lines_f2:
# 	print commit_list_from_csv(line)
