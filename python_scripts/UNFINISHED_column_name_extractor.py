#!/usr/bin/python

# Used this to print the names of each column in the xml. I then made a bash
# script that takes the names of each column (as a csv) and creates a mysql table from it

from BeautifulSoup import BeautifulSoup

tempfilename = "Brand_Catalog_Content_Export(0).xml"

#for i in range (566):
#	filename = "Brand_Catalog_Content_Export(%s).xml" % i
#	soup = BeautifulSoup(open(filename))

soup = BeautifulSoup(open(tempfilename))
for tag in soup.part.findAll(True):
	print(tag.name)
