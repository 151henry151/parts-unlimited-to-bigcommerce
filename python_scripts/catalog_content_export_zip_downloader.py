#!/usr/bin/python

# This script downloads the brand catalog content export zip files

import requests
from BeautifulSoup import BeautifulSoup
import os
#import time
import getpass

def bool_str(s):
	s = s.lower()
	T = ('1', 'true', 'y', 'ye', 'yes', 'yea', 'ya', 'yah', 'yup')
	F = ('0', 'false', 'n', 'no', 'not', 'nope', 'na', 'nah')
	if s in T:
		return True
	elif s in F:
		return False
	else:
		raise VaueError('"%s" is not a recognized yes or no string' % s)

working_directory = "../catalog_content_export_zips"

if os.path.isdir(working_directory):
	os.chdir(working_directory)
	print("Changing working directory to ../catalog_content_export_zips")
	cont = True
else:
	cont = bool_str(raw_input("Could not change working directory. Continue? (y/n)"))

if cont:

	mypasswd = getpass.getpass('Partsnetweb Password:')
	mydlrcode = raw_input("Partsnetweb Dealer Code:")
	myusrname = raw_input("Partsnetweb User Name:")

	coke = dict(user_id=myusrname, dealer_id=mydlrcode, password=mypasswd, form_action='LOGIN')

	baseurl = 'https://www.partsnetweb.com/index.jsp'
	
	otherbaseurl = 'https://www.partsnetweb.com/checkLogin.jsp?redirect='
	secondurl = 'https://www.partsnetweb.com/partSearch/download'
	thirdurl = 'https://www.partsnetweb.com/main.jsp?Nav=Product'
	
	s = requests.Session()
	s.get(baseurl)
	s.post(baseurl, data=coke)
	#time.sleep(5)
	print("getting baseurl")
	s.get(otherbaseurl)
	#time.sleep(5)
	print("checking login...")
	s.get(thirdurl) 
	secondcontent = s.get(thirdurl)
	print("getting download page...")
	#jsesh = s.cookies['JSESSIONID']
	#print(jsesh)
	#secondurl = 'https://www.partsnetweb.com/partSearch/download'
	#time.sleep(5)
	#javapage = requests.get(secondurl)
	with open("main.jsp", "wb") as code:
		code.write(secondcontent.content)
		print("Opening URL as Page Object")
		#print("Waiting 10 seconds for Page Object to download")
	#time.sleep(10)
	soup = BeautifulSoup(open('main.jsp'))
	for p in soup.findAll('input'):
		print("Finding next filename")
		x = p.get('name')
		if x == 'br':
			y = p.get('value')
			branddownload = dict(br=str(y), brandSelected=str(y), exportType='PartMarketingData', exportDisplayName='Brand_Catalog_Content_Export', requestType='brandExportSplash')
			r = s.post(secondurl, data=branddownload)
			with open("Brand_Catalog_Content_Export" + str(y) + ".zip", "wb") as code:
				code.write(r.content)
			print("Saving Brand_Catalog_Content_Export " + str(y) + ".zip...")
			print("Done.")
	print("Brand Catalog Content Export Zip Downloads Complete!")
