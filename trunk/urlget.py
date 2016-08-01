#!/bin/env/python

import json
import time
import urllib2

# Retrieve api tool dump from URL and read it into result
req = urllib2.Request('https://www.dockstore.org:8443/api/v1/tools')
response = urllib2.urlopen(req)
result = response.read()

# Write a json file with the contents of result
json_object = json.loads(result)
with open('stupid.json', 'w+') as outfile:
	outfile.truncate()
	json.dump(json_object, outfile, indent=4, sort_keys=True)

# Iterate through result for specific entries
for project in json_object:
	time.sleep(2)
	
	name = project['toolname']
	toolid = project['toolname']
	print "\nName:", name

	version_list = project['versions']
	version = version_list[0]
	url = version['image']
	print "URL:", url
	
	help_text = project['description']

'''
versions <type 'list'>
description <type 'unicode'>
tooltype <type 'dict'>
url <type 'unicode'>
contains <type 'list'>
meta-version <type 'unicode'>
toolname <type 'unicode'>
organization <type 'unicode'>
id <type 'unicode'>
'''

# for entry in the json dump, create an XML file!
# 	  
# 	  Note: XML req = JSON dump 
# 	  
# 	  tool id = toolname again?
# 	  name = toolname
# 	  
# 	  description = tooltype:description
# 	  
# 	  inputs = 
# 	  format = 
# 	  name = input + count
# 	  type = 
# 	  
# 	  outputs = 
# 	  format = 
# 	  name = output + count
# 	  
'''Should I have some kind of file-extension extraction method for format?'''
# 	  
# 	  URL = versions[1]:image?
# 	  command = python toolRunner.py URL filepath/to/json $inputs $outputs
# 	  
# 	  help = description
# 	  

