#!/bin/env/python

import json
import subprocess
import sys 

subprocess.call(["curl", "-X", "GET", "--header", "'Accept: application/json'", 
	             "https://www.dockstore.org:8443/api/v1/tools/quay.io%2Fljdursi%2Fpcawg-merge-annotate/versions/latest/descriptor?format=CWL", 
	             ">", "Dockstore.cwl"])

subprocess.call(["dockstore", "tool", "convert", "cwl2json", 
	             "--cwl", "Dockstore.cwl", ">Dockstore.json"])

with open('Dockstore.json','r') as infile:
	data = infile.read()

flag = True
for item in sys.argv:
	# Skip the first item in sys.argv (the name of the program)
	# Will probably augment later when URL is passed
	if flag:
		flag = False
		continue
	data = data.replace("fill me in", item, 1)

with open('Dockstore.json','w') as outfile:
	outfile.write(data)

# 
# So, by this point, we've got a JSON file with all of the inputs we could ever want.
# 
# Hurray for that
# 
# Now the current goal is to load said json document, 
# and for all "fill me in", change it to the according URL,
# and output the proper json file
# 