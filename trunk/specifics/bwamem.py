#!/bin/env/python

import json
import os.path
import subprocess
import sys 

# Activate virtual env to run bamstats
activate_this_file = "/home/alex/env/bin/activate_this.py"
execfile(activate_this_file, dict(__file__=activate_this_file))

# Format JSON document based on input
data = ('{  "reads": [{  "path":"' + sys.argv[1] + 
		 '",  "class":"File"  },  {"path":"' + sys.argv[2] + 
		 '",  "class":"File"}  ],  "reference_gz_amb": {"path":'
		 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.amb"'
		 ',"class": "File"  },  "reference_gz_sa": {  "path": '
		 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.sa",'
		 '"class": "File"},  "reference_gz_pac": { "path": '
		 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.pac",'
		 '"class": "File"  },  "reference_gz_ann": {    "path": '
		 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.ann",'
		 '"class": "File"  },  "reference_gz_bwt": {    "path": '
		 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.64.bwt",'
		 '"class": "File"  },  "reference_gz_fai": {    "path": '
		 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz.fai",'
		 '"class": "File"},  "reference_gz": {    "path": '
		 '"http://s3.amazonaws.com/pan-cancer-data/pan-cancer-reference/genome.fa.gz",'
		 '"class": "File"  },  "merged_output_unmapped_bai": {"path": "'
		  + sys.argv[3] +  
		  '","class": "File"  },  "merged_output_bam": {    "path": "' 
		  + sys.argv[4] +  
		  '","class": "File"  },  "merged_output_unmapped_bam": {    "path":"'   
		  + sys.argv[5] +   
		  '","class": "File"  },  "merged_output_bai": {    "path": "' 
		  + sys.argv[6] +
		  '","class": "File"  }}')

parsed = json.loads(data)
filename = 'bwamem.json'

with open(filename, 'w+') as outfile:
	outfile.truncate()
	json.dump(parsed, outfile, indent=4, sort_keys=True)
	filepath = os.path.abspath(filename)
	print "Filepath:", filepath

# Prepare bamstats run command
command = ["dockstore", "tool",	"launch", "--entry", 
 		   "quay.io/pancancer/pcawg-bwa-mem-workflow:2.6.8",
		   "--json", filepath]
result = subprocess.call(command)

print "\nSuccess: ", not bool(result)

sys.exit(not bool(result))