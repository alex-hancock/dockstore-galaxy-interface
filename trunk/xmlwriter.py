#!/bin/env/python

import json
import urllib2
import subprocess
import sys
import yaml

# TODO 
# Add help and description to XML files
# But, for now, minimal product for demonstration

# Convert a url list to a list of 
def ext_conversion(url_list):
    dict = {}
    dict['http://edamontology.org/format_2572'] = 'bam'
    dict['http://edamontology.org/format_3016'] = 'vcf'
    dict['http://edamontology.org/format_3615'] = 'bgzip'
    # Obviously extend this at a later point in time

    extension_list = []
    for url in url_list:
        extension_list.append(dict[url])
    return extension_list

# Retrieve api tool dump from URL and read it into result
req = urllib2.Request('https://www.dockstore.org:8443/api/v1/tools')
response = urllib2.urlopen(req)
text_tools = response.read()
json_tools = json.loads(text_tools)

file_list = []

for tool in json_tools:
    for version_dict in tool['versions']:
        arguments = ""

        # Unsure of how to get latest version
        ver = version_dict['name']
        URL = tool['id'] + ":" + ver

        name = tool['id'].split('/')
        name = name[len(name) - 1]

        print "\n", URL

        # Get CWL file 
        with open(name + '.cwl','w+') as outfile:
            outfile.truncate()
            subprocess.call(["dockstore", "tool", "cwl", "--entry", URL],
                             stdout=outfile)

        # Get extensions from CWL file
        input_list = []
        output_list = []
        with open(name + '.cwl','r+') as infile:
            entry = yaml.load_all(infile)
            try:
                for dic in entry:
                    tool_id = dic['label']
                    name = dic['id']

                    input_versions = dic['inputs']
                    for in_dict in input_versions:
                        if (type(in_dict) == str): 
                            continue
                        if 'format' in in_dict:
                            if type('format') is str:
                                input_list.append(in_dict['format'])

                    outputs = dic['outputs']
                    for out_dict in outputs:
                        if (type(out_dict) == str): 
                            continue
                        if 'format' in out_dict:
                            if type('format') is str:
                                output_list.append(out_dict['format'])
            except:
                print "Yeah, I skipped this one."
                continue
                # If at first you don't succeed...
                # Give up. It's not worth it anyways.

        input_list = ext_conversion(input_list)
        output_list = ext_conversion(output_list)

        infiles = ""
        for count, ext in enumerate(input_list):
            label = "$input" + str(count + 1)
            arguments += label + " "
            infiles += '    <param format="' + ext + '" name="' + \
                                        label + '" type="data"/>\n'

        outfiles = ""
        for count, ext in enumerate(output_list):
            label = "$output" + str(count + 1)
            arguments += label + " "
            outfiles += '    <data format="' + ext + '" name="' + label + '"/>\n'

        # I'm actually pretty okay with this long string... as long as it works
        string = \
            '<tool id="' + tool_id + '" name="' + name + '" version="' + ver + '" >' + \
            '\n  <command interpreter="python">toolRunner.py ' + URL + ' ' + arguments + '</command>' + \
            '\n  <inputs>\n' + infiles + \
            '  </inputs>' + \
            '\n  <outputs>\n' + outfiles + \
            '  </outputs>' + \
            '\n</tool>\n'

        filename = name + "_" + ver + '.xml'
        file_list.append(filename)
        with open(filename,'w') as outfile:
            outfile.write(string)

        # Do I have to register in config automatically? 
        # That'd probably be a good idea

register = ""
for label in file_list:
    register += '    <tool file="myTools/' + label + '" />\n'

folder = '  <section id="mytools" name="myTools">\n' + register + '  </section>\n'

# Somehow get to config folder...

with open("../../config/tool_conf.xml.sample","r") as infile:
    with open("../../config/tool_conf.xml","w") as outfile:
        outfile.truncate()
        for line in infile: 
            if "toolbox monitor" in line:
                outfile.write(line)
                outfile.write(folder)
                continue

            outfile.write(line)