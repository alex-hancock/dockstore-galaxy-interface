#!/bin/env/python

import urllib2

manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
manager.add_password(None, 'https://www.dockstore.org:8443/api/v1/tools', 'login', 'key')
handler = urllib2.HTTPBasicAuthHandler(manager)

director = urllib2.OpenerDirector()
director.add_handler(handler)

req = urllib2.Request('https://www.dockstore.org:8443/api/v1/tools', 
					        headers = {'Accept' : 'application/xml'})

result = director.open(req)
# result.read() will contain the data
# result.info() will contain the HTTP headers

# To get say the content-length header
length = result.info()['Content-Length']