#!/bin/env/python

import json
import sys

data = '{ "bam_input": { "class": "File", "path": "' + str(sys.argv[1]) + '" }, "bamstats_report": { "class": "File", "path": "' + str(sys.argv[2])+ '"} }'
parsed = json.loads(data)
with open('dockstore.json', 'w+') as outfile:
	json.dump(parsed, outfile, indent=4, sort_keys=True)