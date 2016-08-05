#!/bin/env/python

import json
import urllib2
import subprocess
import sys
import yaml

# Retrieve api tool dump from URL and read it into result
req = urllib2.Request('https://www.dockstore.org:8443/api/v1/tools')
response = urllib2.urlopen(req)
text_tools = response.read()
json_tools = json.loads(text_tools)

url_list = []



for tool in json_tools:
	for version_dict in tool['versions']:

		# FIXME
		# Unsure of how to get latest version
		ver = version_dict['name']
		URL = tool['id'] + ":" + ver

		print "URL of current version:", URL

		# Get CWL file 
		with open('Dockstore.cwl','w') as outfile:
			outfile.truncate()
			subprocess.call(["dockstore", "tool", "cwl", "--entry", URL],
				  		  	 stdout=outfile)

		# Get extensions from CWL file
		with open('Dockstore.cwl','r') as infile:
			entry = yaml.load_all(infile)
			try:
				for dic in entry:

					for file_entry in dic['inputs']:
						if 'format' in file_entry:
							url_list.append(URL + " - " + file_entry['format'])

					for file_entry in dic['outputs']:
						if 'format' in file_entry:
							url_list.append(URL + " - " + file_entry['format'])
			except:
				continue

for url in url_list:
	print url
