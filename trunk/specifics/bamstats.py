#!/bin/env/python

import json
import os.path
import subprocess
import sys 

print "Input file:", sys.argv[1]
print "Output file:", sys.argv[2]

# Activate virtual env to run bamstats
activate_this_file = "/home/alex/env/bin/activate_this.py"
execfile(activate_this_file, dict(__file__=activate_this_file))

# Format JSON document based on input
data = '{ "bam_input": { "class": "File", "path": "' + str(sys.argv[1]) + '" }, "bamstats_report": { "class": "File", "path": "' + str(sys.argv[2])+ '"} }'
parsed = json.loads(data)
filename = 'bamstats.json'

with open(filename, 'w+') as outfile:
	outfile.truncate()
	json.dump(parsed, outfile, indent=4, sort_keys=True)
	filepath = os.path.abspath(filename)
	print "Filepath:", filepath

# Prepare bamstats run command
command = ["dockstore", "tool",	"launch", "--entry", 
 		   "quay.io/briandoconnor/dockstore-tool-bamstats:1.25-5",
		   "--json", filepath]
result = subprocess.call(command)

print "\nSuccess: ", not bool(result)

sys.exit(not bool(result))