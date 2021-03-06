#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""


import urllib.request, urllib.error, urllib.parse
import ssl
from cdb.common.client.cdbHttpsConnection import CdbHttpsConnection

class CdbHttpsHandler(urllib.request.HTTPSHandler):

    def https_open(self, req):
        return self.do_open(CdbHttpsConnection,req)

#######################################################################
# Testing.

if __name__ == '__main__':
    from cdb.common.utility.configurationManager import ConfigurationManager 
    cm = ConfigurationManager.getInstance()
    cm.setSslCaCertFile("/home/sveseli/Work/CDB/etc/ssl/cacert.pem")

    print("Installing opener")
    opener = urllib.request.build_opener(CdbHttpsHandler)
    urllib.request.install_opener(opener)

    url = "https://zagreb.svdev.net:10232/cdb/directory/list?path=/tmp"
    print("Opening URL: ", url)
    #context = ssl.create_default_context(cafile="/home/sveseli/Work/CDB/etc/ssl/cacert.pem")
    #ssl._create_default_https_context = ssl._create_unverified_context
    #f = urllib2.urlopen(url, context=context)
    f = urllib.request.urlopen(url)
    print(f.code)
    print(f.read())

