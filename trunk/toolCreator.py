#!/bin/env/python

import json
import os
import re
import subprocess
import sys
import urllib2
import yaml

'''
Problems/Assumptions
    a) Add help and description to XML files 

    b) Retrieving for all versions is slow... way to find only most recent?

    c) Java exceptions that don't break the whole program...
        * These are problems with the CWL files or some problem with the 
          URL I'm passing to the dockstore cwl retrieval tool

    d) Reliant on the format tag in the CWL file

    e) Path to config file should be guaranteed, but also worth noting
'''
# Remove # symbol from inputs
def hashremove(string):
    return re.sub('[#]', '', string)

# Convert a url list to a list of extensions
def ext_conversion(url_list):
    url_to_ext = {}
    url_to_ext['http://edamontology.org/format_2572'] = 'bam'
    url_to_ext['http://edamontology.org/format_3016'] = 'vcf'
    url_to_ext['http://edamontology.org/format_3615'] = 'bgzip'
    url_to_ext['txt'] = 'txt'
    # Obviously extend this at a later point in time

    extension_list = []
    for url in url_list:
        extension_list.append(url_to_ext[url])
    return extension_list

# Retrieve api tool dump from URL and read it into result
req = urllib2.Request('https://www.dockstore.org:8443/api/v1/tools')
response = urllib2.urlopen(req)
text_tools = response.read()
json_tools = json.loads(text_tools)

file_list = []
for tool in json_tools:
    for version_dict in tool['versions']:

        # Definitions
        arguments = ""
        input_ext_list = []
        output_ext_list = []
        input_label_list = []
        output_label_list = []        
        ver = version_dict['name']
        URL = tool['id'] + ":" + ver
        name = tool['id'].split('/')
        name = name[len(name) - 1]
        cwlsource = name + "_" + ver + '.cwl'

        print "\n" + name + "_" + ver

        # Bad URLs, discuss later
        bad_URL_list = ["quay.io/ljdursi/pcawg-merge-annotate:1.0.0", "quay.io/mr_c/khmer:docker-2.0"]
        if URL in bad_URL_list:
            #print "\tBad/Empty CWL file"
            continue

        # Retrieve CWL file 
        with open(cwlsource,'w') as outfile:
            subprocess.call(["dockstore", "tool", "cwl", "--entry", URL],
                             stdout=outfile)

        # Get extensions from CWL file
        with open(cwlsource,'r+') as infile:
            entry = yaml.load_all(infile)

            for dic in entry:
                if 'label' in dic and 'id' in dic:
                    tool_id = dic['label']
                    name = dic['id']
                else:
                    tool_id = name

                input_versions = dic['inputs']
                for in_dict in input_versions:
                    if (type(in_dict) == str): 
                        continue
                    if 'format' in in_dict:
                        if type('format') is str:
                            string = hashremove(in_dict['id'])
                            input_label_list.append(string)
                            input_ext_list.append(in_dict['format'])
                    elif 'type' in in_dict:
                        if in_dict['type'] == "File":
                            string = hashremove(in_dict['id'])
                            input_label_list.append(string)
                            input_ext_list.append("txt")

                outputs = dic['outputs']
                for out_dict in outputs:
                    if (type(out_dict) == str): 
                        continue
                    if 'format' in out_dict:
                        if type('format') is str:
                            string = hashremove(out_dict['id'])
                            output_label_list.append(string)
                            output_ext_list.append(out_dict['format'])
                    elif 'type' in out_dict:
                        if out_dict['type'] == "File":
                            string = hashremove(out_dict['id'])
                            output_label_list.append(string)
                            output_ext_list.append("txt")

        # Convert URLs to extensions, create the XML tags
        input_ext_list = ext_conversion(input_ext_list)
        output_ext_list = ext_conversion(output_ext_list)
        infiles = ""
        for count, ext in enumerate(input_ext_list):
            label = input_label_list[count]
            arguments += "$" + label + " "
            infiles += '    <param format="' + ext + '" name="' + \
                                        label + '" type="data"/>\n'
        outfiles = ""
        for count, ext in enumerate(output_ext_list):
            label = output_label_list[count]
            arguments += "$" + label + " "
            outfiles += '    <data format="' + ext + '" name="' + label + '"/>\n'

        # Create final XML segment, write out
        filename = name + "_" + ver
        string = \
            '<tool id="' + tool_id + '" name="' + filename + '" version="' + ver + '" >' + \
            '\n  <command interpreter="python">toolRunner.py ' + URL + ' ' + arguments + '</command>' + \
            '\n  <inputs>\n' + infiles + \
            '  </inputs>' + \
            '\n  <outputs>\n' + outfiles + \
            '  </outputs>' + \
            '\n</tool>\n'
        filename += ".xml"
        with open(filename,'w') as outfile:
            outfile.write(string)
            file_list.append(filename)

        # Cleanup empty/unwanted files
        subprocess.call(['rm', cwlsource])
        if len(input_ext_list) == 0 and len(output_ext_list) == 0:
            os.remove(filename)

register = ""
for label in file_list:
    register += '    <tool file="myTools/' + label + '" />\n'
folder = '  <section id="mytools" name="myTools">\n' + \
            register + \
         '  </section>\n'
with open("../../config/tool_conf.xml.sample","r") as infile:
    with open("../../config/tool_conf.xml","w") as outfile:
        for line in infile: 
            if "toolbox monitor" in line:
                outfile.write(line)
                outfile.write(folder)
                continue

            outfile.write(line)