#!/usr/bin/python

# Watch out! this script will delete any csv files in your working directory!
# this script logs in to lemans.com, downloads 
# a zip file with the basepricefile.csv in it,
# extracts that csv file, then takes that csv file and uses it to 
# populate a mysql database with that data

# will need to modify the csvdataimport.sql file to incorporate
# the REPLACE and IGNORE keywords so that we can use it to update
# as opposed to initial creation

import sqlite3
from sqlite3 import OperationalError
import requests
import io
import zipfile
import subprocess
import glob
import os
import getpass
from cStringIO import StringIO

##This changes current working directory 
os.chdir("../base_price_files")

##This clears out any old csv files in the working directory
filenames = glob.glob('BasePriceFile.csv')
for filename in filenames:
    os.remove(filename)

##These are the login credentials
mypsswd = getpass.getpass('Partsnetweb Password:')
mydlrcode = raw_input("Partsnetweb Dealer Code:")
myusrname = raw_input("Partsnetweb User ID:")

##This logs in and obtains the token
payload = {'rememberMe': 'on', 'password': mypsswd, 'dealerCode': mydlrcode, 'dm': '4', 'userName': myusrname}
loginurl = 'https://www.lemansnet.com/login'
r = requests.post(loginurl, data=payload)
token = r.headers['loginToken']

##xmlpayload is a one-time string, it will be the same any time this is run
xmlpayload = """<pricing><whoForDealer><dealerCode>MET087</dealerCode></whoForDealer><rememberPreferences>1</rememberPreferences></pricing>"""

##This will use the token to request the pricefile zip archive
pricingurl = 'https://www.lemansnet.com/pricing/2013/pos'
headers = {'loginToken': token, 'Content-Type': 'text/xml; charset=utf-8'}
d = requests.post(pricingurl, data=xmlpayload, headers=headers)

##This extracts the CSV file from the ZIP file that we just requested
##into our current directory.  

d_file = StringIO(d.content)
if zipfile.is_zipfile(d_file):
    z = zipfile.ZipFile(d_file)
    z.extractall()
else:
    print(d.content)

