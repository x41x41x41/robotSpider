#!/usr/bin/python
import sys, os, argparse, urllib2
from urllib2 import Request
#from urllib.request import urlopen
from multiprocessing import Pool

def findftp(domain):
	domain = domain.strip()
    
	# TAKE A LOOK FOR robots.txt file
	# Try to download http://target.tld/robots.txt
	request = Request('http://' + domain + "/robots.txt")
	req = urllib2.urlopen(request)
	answer = req.read()

	# Write match to OUTPUTFILE
	print "done"
	return
    
domains = findftp("google.com");
