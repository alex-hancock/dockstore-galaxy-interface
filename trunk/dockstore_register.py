import json
import os
import re
import subprocess
import urllib2
import yaml

# Given a dictionary of something or other, 
# iterate through CWL file and record formats required
def extension_retrieval(dict_list):
    label_list = []
    ext_list = []
    for io_dict in dict_list:
        if (type(io_dict) == str): 
            continue
        if 'format' in io_dict:
            if type('format') is str:
                string = re.sub('[#]', '', io_dict['id'])
                label_list.append(string)
                ext_list.append(io_dict['format'])
        elif 'type' in io_dict:
            if io_dict['type'] == "File":
                string = re.sub('[#]', '', io_dict['id'])
                label_list.append(string)
                ext_list.append("txt")

    return label_list, ext_list

# Convert a url list to a list of extensions
# Manual conversion, hope to automate at some point
def ext_conversion(url_list):
    # Initialize a dictionary
    url_to_ext = {}

    # Define some recognizable formats
    url_to_ext['http://edamontology.org/format_2572'] = 'bam'
    url_to_ext['http://edamontology.org/format_3016'] = 'vcf'
    url_to_ext['http://edamontology.org/format_3615'] = 'zip'

    # If it's not a recognizable format URL, default to generic txt
    url_to_ext['txt'] = 'txt'

    # Convert URL list to extensions
    extension_list = []
    for url in url_list:
        extension_list.append(url_to_ext[url])
    return extension_list

# Retrieve api tool dump from URL and read it into json_tools
req = urllib2.Request('https://www.dockstore.org:8443/api/v1/tools')
response = urllib2.urlopen(req)
text_tools = response.read()
json_tools = json.loads(text_tools)

# Iterate through each tool and each version of each tool
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
        bad_URL_list = ["quay.io/ljdursi/pcawg-merge-annotate:1.0.0", 
                        "quay.io/mr_c/khmer:docker-2.0"]

        # Edit these "dockstore-tool-" from name
        if "dockstore-tool-" in name:
            name = name[15:]
        cwlsource = name + '.cwl'

        # Skip bad URLs in API dump
        if URL in bad_URL_list:
            continue

        # Retrieve CWL file using URL
        with open(cwlsource,'w') as outfile:
            subprocess.call(["dockstore", "tool", "cwl", "--entry", URL], stdout=outfile)
            if os.stat(cwlsource).st_size == 0:
                print "\n" + name + "_" + ver
                print "\t-> Problem with CWL retrieval"

        # Get extensions from CWL file
        with open(cwlsource,'r+') as infile:
            entry = yaml.load_all(infile)

            for dic in entry:
                if 'label' in dic and 'id' in dic:
                    tool_id = dic['label']
                    name = dic['id']
                else:
                    tool_id = name

                input_label_list, input_ext_list = extension_retrieval(dic['inputs'])                
                output_label_list, output_ext_list = extension_retrieval(dic['outputs'])

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
        filename = name
        string = \
            '<tool id="' + tool_id + '" name="' + filename + '" version="' + ver + '" >' + \
            '\n  <command interpreter="python">runner.py ' + URL + ' ' + arguments + '</command>' + \
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
# Should use current folder as registry location
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
