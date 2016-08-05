#!/bin/env/python

import json
import os
import os.path
import subprocess
import sys 

'''
Okay, real talk, there's some bad programming here. 

First, my solution for editing bad lines from the json file 
is by looking for mem_gb and just not writing the line... That can't be good.

Secondly, there's a lot of temp files (only two now, but still) being created 
that probably don't need to exist, but Dockstore's converter takes one and 
produces another, so there's at least one that isn't my fault. Moreover, they 
should be removed.
'''

# Activate virtual env to run bamstats
this_file = "../../../env/bin/activate_this.py"
execfile(this_file, dict(__file__=this_file))

commandstr = sys.argv[1]

# Call dockstore to retrieve json package, including cwl
with open('Dockstore.cwl','w') as outfile:
	subprocess.call(["dockstore", "tool", "cwl", "--entry", commandstr],
		  		  	 stdout=outfile)

# Convert cwl to json
with open('Dockstore.json','w') as outfile:
	subprocess.call(["dockstore", "tool", "convert", "cwl2json", "--cwl", "Dockstore.cwl"], 
		  		  	 stdout=outfile)

data = ""
with open('Dockstore.json','r') as infile:
	for line in infile:
		# This is a very basic, probably ineffective fix
		# for what might be a serious problem. 
		if "mem_gb" not in line:
			data += line

for value, item in enumerate(sys.argv):
	# Skip name of program and URL
	if value < 2:
		continue
	data = data.replace("fill me in", item, 1)

with open('Dockstore.json','w') as outfile:
	outfile.write(data)
	filepath = os.path.abspath('Dockstore.json')

command = ["dockstore", "tool",	"launch", "--entry", commandstr, "--json", filepath]
result = subprocess.call(command)

sys.exit(not bool(result))