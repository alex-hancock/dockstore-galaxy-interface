#!/bin/env/python

import yaml
import subprocess

commandstr = "quay.io/briandoconnor/dockstore-tool-bamstats:1.25-5"
'''
with open('Dockstore.cwl','w') as outfile:
	subprocess.call(["dockstore", "tool", "cwl", "--entry", commandstr],
		  		  	 stdout=outfile)
'''
with open('Dockstore.cwl','r') as infile:
	entry = yaml.load_all(infile)
	for dic in entry:
	    tool_id = dic['label']
	    name = dic['id']

	    req = dic['requirements'][0]
	    URL = req['dockerPull']

	    input_list = dic['inputs']
	    for in_dict in input_list:
	    	if 'format' in in_dict:
		    	print in_dict['format']

	    outputs = dic['outputs']
	    for out_dict in outputs:
	    	print out_dict['format']