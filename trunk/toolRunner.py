#!/bin/env/python

import json
import os
import os.path
import subprocess
import sys 

'''
Problems/Assumptions:

a) Getting the directory for the virtual environment is sketchy

b) Should we remove Dockstore.cwl?

c) That ignore mem_gb is a really bad fix. Should I do something about that?
'''

# Activate virtual env to run bamstats
curpath = os.getcwd()
dir_list = curpath.split('/')
path = ""
for directory in dir_list:
	# This path hunt assumes that galaxy is in "/home/user"
	if directory == "galaxy":
		break
	path += "/" + directory
this_file = path + "/env/bin/activate_this.py"
execfile(this_file, dict(__file__=this_file))

# This is where the URL is passed when toolRunner is called
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

# Ignore program name and URL, 
# retrieve all input and output paths
for value, item in enumerate(sys.argv):
	# Skip name of program and URL
	if value < 2:
		continue
	data = data.replace("fill me in", item, 1)

# Write the filled-in Dockstore.json file
with open('Dockstore.json','w') as outfile:
	outfile.write(data)
	filepath = os.path.abspath('Dockstore.json')

# Call the command
command = ["dockstore", "tool",	"launch", "--entry", commandstr, "--json", filepath]
result = subprocess.call(command)

sys.exit(not bool(result))