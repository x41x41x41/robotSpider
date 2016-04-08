#!/usr/bin/python
import sys, os, argparse, urllib2
from urllib2 import Request
#from urllib.request import urlopen
from multiprocessing import Pool

def findftp(domain):
	domain = domain.strip()
    
    	try:
		# TAKE A LOOK FOR robots.txt file
		# Try to download http://target.tld/robots.txt
		request = Request('http://' + domain + "/robots.txt")
		req = urllib2.urlopen(request)
		answer = req.read()

		# Write match to OUTPUTFILE
		fHandle = open(OUTPUTFILE,'a')
		fHandle.write(domain + ", robots.txt, "+req.headers.get('content-length')+"\n")
		fHandle.close()
		print("[*] Found robots: " + domain)
		return

	except Exception as e:     
        	print("[*] Nope: " + domain)
    

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='domains.txt', help='input file')
    parser.add_argument('-o', '--outputfile', default='output.txt', help='output file')
    parser.add_argument('-t', '--threads', default=200, help='threads')
    args = parser.parse_args()

    DOMAINFILE=args.inputfile
    OUTPUTFILE=args.outputfile
    MAXPROCESSES=int(args.threads)

    print("Scanning...")
    pool = Pool(processes=MAXPROCESSES)
    domains = open(DOMAINFILE, "r").readlines()
    pool.map(findftp, domains)
    print("Finished")
