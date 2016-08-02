#!/bin/env/python

import json
import os
import os.path
import subprocess
import sys 

'''
Okay, real talk, there's some bad programming here. 

First of all, I'm using curl instead of Python's urllib2 library,
mostly because the file process seemed more intuitive to me, and 
I don't have the experience with urllib2 to be reasonable.

Second of all, I just pipe the stderr of that curl command to /dev/null/
because Galaxy flips out anytime it sees stderr from it... I should fix that 
at some point.

Third and finally, there's a lot of temp files being created that probably 
don't need to exist, but Dockstore's converter takes one and produces another, 
so there's at least one that isn't my fault. Moreover, they should probably
be removed.
'''

# Call curl to retrieve json package, including cwl
FNULL = open(os.devnull, 'w')
with open('temp.json','w') as outfile:
	subprocess.call(["curl", "-X", "GET", "--header", "'Accept: application/json'", 
		             "https://www.dockstore.org:8443/api/v1/tools/quay.io%2Fbriandoconnor%2Fdockstore-tool-bamstats/versions/latest/descriptor?format=CWL"],
	    	         stdout=outfile, stderr=FNULL)
FNULL.close()

# Need code here to process the json output of the curl command
with open('temp.json','r') as infile:
	json_object = json.load(infile)

# Extract CWL code from JSON dict and write to file
content_cwl = json_object['descriptor']
with open('Dockstore.cwl','w') as outfile:
	outfile.write(content_cwl)

# Convert cwl to json
with open('Dockstore.json','w') as outfile:
	subprocess.call(["dockstore", "tool", "convert", "cwl2json", "--cwl", "Dockstore.cwl"], 
		  		  	 stdout=outfile)

data = ""
with open('Dockstore.json','r') as infile:
	for line in infile:
		if "mem_gb" not in line:
			data += line

count = 0
for item in sys.argv:
	# Skip the first item in sys.argv (the name of the program)
	if count < 1:
		count += 1
		continue
	data = data.replace("fill me in", item, 1)

with open('Dockstore.json','w') as outfile:
	outfile.write(data)
	filepath = os.path.abspath('Dockstore.json')

commandstr = "quay.io/briandoconnor/dockstore-tool-bamstats:1.25-5"
#commandstr = sys.argv[2]
command = ["dockstore", "tool",	"launch", "--entry", commandstr, "--json", filepath]
result = subprocess.call(command)

sys.exit(not bool(result))