#!/usr/bin/python

import sys
import time
from time import gmtime, strftime
import datetime
import subprocess
from uuid import uuid4
import os.path


try:
  target = str(sys.argv[1])
  #name = str(sys.argv[2])
  context = str(sys.argv[2])
  bsp_type = str(sys.argv[3])
  uid = str(uuid4())
  test_type = "ptest"
  commit = str(sys.argv[4])
  build_date = str(sys.argv[5])
  img_type = str(sys.argv[6])
  #name = target.split(".")[-1]
  name = target.split("/")[-1].replace("pass.","").replace("fail.","")
except IndexError, NameError:
	print "Usage: ptest2bundle <file> <context> <bsp_type> <commit> <date> <img_type> \n Example: ptest2bundle pass.fail.bash yocto-1.7.rc1 sugarbay 8ac8eca2e3bd8c78e2b31ea974930ed0243258a3 2014-09-24 core-image-lsb-sdk"
	exit(1)

year = time.strftime("%Y-%m-%e", gmtime())
hour = time.strftime("%H:%M:%S", gmtime())

test_list = []
test_list_string = ""
test_id = ""
result = ""
msg = ""

if not os.path.isfile(target):
  print "Cannot find log file!"
  exit(1)

with open(target, 'r') as content_file:
    content = content_file.read()

file_content = subprocess.check_output("openssl enc -base64 -in "+target+" -out "+target+".enc && cat "+target+".enc", shell=True)

content = content.split("\n")    

for i in xrange (len(content)-1):
  result = content[i].split(":  ")[0]
  try:
      test_id = content[i].split(":  ")[1]
  except:
      test_id = content[i].split(": ")[1]
      result = content[i].split(": ")[0]  
  test_id = test_id.replace('\"', '\\\"')

  test_template = """    {
          "result": "%s",
          "test_case_id": "%s",
          "message": ""
        },
  """ % (result, test_id)
  test_list.append(test_template)

for i in xrange(len(test_list)):
	test_list_string += test_list[i]

test_list_string = test_list_string[:test_list_string.rfind('\n')]
test_list_string = test_list_string[:test_list_string.rfind(',')]
file_content = file_content.replace('\n', '')  

json = """{
 "test_runs": [
    {
    "software_context": {
        "image": {
          "name": "%s"
        }
    },
    "test_results": [
    	%s
      ],
      "attributes": {
        "target": "%s",
        "commit": "%s",
        "date": "%s",
        "image type": "%s"
      },
      "attachments": [
      {
        "content": "%s",
        "pathname": "%s",
        "mime_type": "text/plain"
      }
      ],
      "analyzer_assigned_uuid": "%s",
      "analyzer_assigned_date": "%sT%sZ",
      "test_id": "%s-%s",
      "time_check_performed": false
    }],
  "format": "Dashboard Bundle Format 1.7"
}""" % (context,test_list_string ,bsp_type ,commit ,build_date, img_type, file_content ,name, uid, year, hour, name, test_type)

#print json
bundlename = name+"_"+bsp_type+"_"+test_type+"_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")+".bundle"
with open(bundlename, 'w') as the_file:
    the_file.write(json)

transfer_file = subprocess.check_output("scp "+bundlename+" root@10.237.112.80:/var/lib/lava/dispatcher/tmp/bundle_streams/ptest/", shell=True)
print transfer_file
submit_file = subprocess.check_output("ssh root@10.237.112.80 \"cd /var/lib/lava/dispatcher/tmp/bundle_streams/ptest/ && lava-tool put --dashboard-url=http://localhost/RPC2/ "+bundlename.split("/")[-1]+" /anonymous/ptest-"+name+"/\"", shell=True)
print submit_file
analyze_bundle = subprocess.check_output("ssh root@10.237.112.80 \"/var/lib/lava/dispatcher/tmp/bundle_streams/bundle_compare.py "+bsp_type+" "+test_type+" "+name+" "+build_date+" /var/lib/lava/dispatcher/tmp/bundle_streams/ptest\"", shell=True)
print analyze_bundle
