#!/usr/bin/python
import sys, os, argparse, urllib2
from urllib2 import Request
#from urllib.request import urlopen
from multiprocessing import Pool

def process(domain, req, answer):
	print("[*] Found robots: " + domain + " :: " + str(req.code))
	
	# Lets process the output
	
	## General File Statistics
	responseLines = len(answer.split('\n'))
	responseCharacters = len(answer)
	
	## UserAgents
	responseUseragents = answer.count("User-agent")
	
	## Sitemaps
	responseSitemaps = answer.count("Sitemap")
	
	## Disallows and Allows
	responseAllows = answer.count("Allow")
	responseDisallows = answer.count("Disallow")
	
	# Write match to OUTPUTFILE
	fHandle = open(SUMMARYFILE,'a')
	#domain, file, response, lines, characters, useragents, sitemaps, allows, disallows
	fHandle.write(domain + ", robots.txt, " + str(req.code) + ", " + str(responseLines) + ", " + str(responseCharacters) + ", " + str(responseUseragents) + ", " + str(responseSitemaps) + ", " + str(responseAllows) + ", " + str(responseDisallows) + "\n" )
	fHandle.close()
	
	#Process line by line now
	responseLines = answer.split('\n')
	for responseLine in responseLines:
		#print responseLine
		if "user-agent:" in responseLine.lower():
			useragent = responseLine.lower().replace("user-agent:", "").strip()
	                # Write match to OUTPUTFILE
        		fHandle = open(USERAGENTFILE, 'a')
	                fHandle.write(domain + ", " + useragent + "\n")
       			fHandle.close()
			#print useragent
		elif "disallow:" in responseLine.lower():
			type = "disallow"
			directory = responseLine.lower().replace("disallow:", "").strip()
                        # Write match to OUTPUTFILE
                        fHandle = open(RULESFILE, 'a')
                        fHandle.write(domain + ", " + useragent + ", " + type + ", "+ directory + "\n")
                        fHandle.close()
                elif "allow:" in responseLine.lower():
                        type = "allow"
                        directory = responseLine.lower().replace("allow:", "").strip()
                        # Write match to OUTPUTFILE
                        fHandle = open(RULESFILE, 'a')
                        fHandle.write(domain + ", " + useragent + ", " + type + ", "+ directory + "\n")
                        fHandle.close()
                elif "sitemap:" in responseLine.lower():
                        sitemap = responseLine.lower().replace("sitemap:", "").strip()
                        # Write match to OUTPUTFILE
                        fHandle = open(SITEMAPFILE, 'a')
                        fHandle.write(domain + ", " + sitemap + "\n")
                        fHandle.close()
	return

def findftp(domain):
	domain = domain.strip()
    
	try:
		# TAKE A LOOK FOR robots.txt file
		# Try to download http://target.tld/robots.txt
		print("[*] Scan (1st try): " + domain)
        	headers = { 'User-Agent' : 'Mozilla/5.0' }
		request = Request('http://' + domain + "/robots.txt", None, headers)
		req = urllib2.urlopen(request)
		answer = req.read()
		process(domain, req, answer)
		
		return

	except Exception as e:   
		# Not really worried about it at this point
		print("[*] Nope (1st try): " + domain)
	
		# If it errored lets try something special (cough youtube.com cough)
		try:
			print("[*] Scan (2nd try): " + domain)
			headers = { 'User-Agent' : 'Mozilla/5.0' }
			request = Request('http://' + domain + "/", None, headers)
			req = urllib2.urlopen(request)
			actualdomain = req.geturl()
			
		except Exception as e:  
			fHandle = open(SUMMARYFILE,'a')
			#domain, file, response, lines, characters, useragents, sitemaps, allows, disallows
			fHandle.write(domain + ", , " + str(e) + " " + req.geturl() + ", , , , , , \n")
			fHandle.close()
	        	print("[*] Nope (2nd try): " + domain)
	        	
	        	return
	        	
		# Then reperform the action
		try:
			# TAKE A LOOK FOR robots.txt file
			# Try to download http://target.tld/robots.txt
			print("[*] Scan (3rd try): " + domain)
	        	headers = { 'User-Agent' : 'Mozilla/5.0' }
			request = Request(actualdomain+"/robots.txt", None, headers)
			req = urllib2.urlopen(request)
			answer = req.read()
			process(domain, req, answer)
			
			return
		
		except Exception as e:  
			fHandle = open(SUMMARYFILE,'a')
			#domain, file, response, lines, characters, useragents, sitemaps, allows, disallows
			fHandle.write(domain + ", , " + str(e) + " " + req.geturl() + ", , , , , , \n")
			fHandle.close()
	        	print("[*] Nope (3rd try): " + domain)
	        	
	        	return
    

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputfile', default='domains.txt', help='input file')
    parser.add_argument('-t', '--threads', default=200, help='threads')
    args = parser.parse_args()

    DOMAINFILE = args.inputfile
    SUMMARYFILE = os.path.splitext(args.inputfile)[0]+"_summary.csv"
    USERAGENTFILE = os.path.splitext(args.inputfile)[0]+"_useragents.csv"
    SITEMAPFILE = os.path.splitext(args.inputfile)[0]+"_sitemaps.csv"
    RULESFILE = os.path.splitext(args.inputfile)[0]+"_rules.csv"
    MAXPROCESSES=int(args.threads)

    print("Scanning...")
    #setup file
    fHandle = open(SUMMARYFILE,'a')
    fHandle.write("domain, file, response, lines, characters, useragents, sitemaps, allows, disallows \n")
    fHandle.close()
    fHandle = open(USERAGENTFILE,'a')
    fHandle.write("domain, useragent \n")
    fHandle.close()
    fHandle = open(RULESFILE,'a')
    fHandle.write("domain, useragent, type, directory \n")
    fHandle.close()
    fHandle = open(SITEMAPFILE,'a')
    fHandle.write("domain, url \n")
    fHandle.close()
    pool = Pool(processes=MAXPROCESSES)
    domains = open(DOMAINFILE, "r").readlines()
    pool.map(findftp, domains)
    print("Finished")
