#!/bin/env/python

import subprocess
import sys

with open('thing.txt','r') as infile:
	data = infile.read()

flag = True
for item in sys.argv:
	if flag:
		flag = False
		continue
	data = data.replace("thing", item, 1)

with open('thing.txt','w+') as outfile:
	outfile.write(data)

subprocess.call(['cat', 'thing.txt'])