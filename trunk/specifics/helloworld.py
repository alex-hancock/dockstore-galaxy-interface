#!/bin/env/python

import argparse

parser = argparse.ArgumentParser()
#parser.add_argument('inputfile')
parser.add_argument('outputfile')
args = parser.parse_args()

# Read file to other file

#with open(args.inputfile, "r") as infile:
with open(args.outputfile, "w") as outfile:
	#for line in infile:
	#	print line.strip("\n")
	outfile.write("I can print to a file and track it!")

	#print "\nHello, world!\n"
