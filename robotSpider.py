#!/usr/bin/python
import sys, os, argparse, urllib2
from urllib2 import Request
#from urllib.request import urlopen
from multiprocessing import Pool

def findftp(domain):
	domain = domain.strip()
    
    	try:
		# TAKE A LOOK FOR FTP Configuration file
		# Try to download http://target.tld/sftp-config.json
		request = Request('http://' + domain + "/sftp-config.json")
		req = urllib2.urlopen(request)
		answer = req.read(200).decode()

		# Check if refs/heads is in the file
		if('refs/heads' in answer):
		    # Write match to OUTPUTFILE
		    fHandle = open(OUTPUTFILE,'a')
		    fHandle.write(domain + ", sftp-config.json, "+req.headers.get('content-length')+"\n")
		    fHandle.close()
		    print("[*] Found config: " + domain)
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
