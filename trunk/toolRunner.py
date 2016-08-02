#!/bin/env/python

import json
import os.path
import subprocess
import sys 

def activate_virtualenv():
	# Activate virtual env to run bamstats
	activate_this_file = "/~/env/bin/activate_this.py"
	execfile(activate_this_file, dict(__file__=activate_this_file))

def json_file_creation(filename):
	# Format JSON document based on input
	data = ('''JSON DATA GOES HERE''')

	parsed = json.loads(data)
	#filename = 'bwamem.json'
	#Somehow automate name of .json file
	filename = 'bwamem.json'

	with open(filename, 'w+') as outfile:
		outfile.truncate()
		json.dump(parsed, outfile, indent=4, sort_keys=True)
		filepath = os.path.abspath(filename)
		print "Filepath:", filepath

activate_virtualenv()

commandstr = "quay.io/pancancer/pcawg-bwa-mem-workflow:2.6.8"
#commandstr = sys.argv[2]
command = ["dockstore", "tool",	"launch", "--entry", commandstr, "--json", filepath]
result = subprocess.call(command)

sys.exit(not bool(result))