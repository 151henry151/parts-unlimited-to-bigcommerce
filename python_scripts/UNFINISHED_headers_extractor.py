#!/usr/bin/python

# This script should create a CSV file from the headers, which
# we will then pass to our table initiator to create a mysql
# database with the appropriate column names

# it actually just prints the headers
# i manually made a csv from it by printing copying and pasting
# then put in the commas

from BeautifulSoup import BeautifulSoup

filename = "Brand_Catalog_Content_Export(0).xml"

soup = BeautifulSoup(open(filename))

#print(soup.prettify())

for part in soup.findAll('part'):
	print(part.prettify())
	#print(part)
	#print("Next Part")
	#print(part.partnumber.string, part.punctuatedpartnumber.string, part.partstatusdescr.string)
#for partimage in soup.findAll('partimage'):
#	if partimage.string != None:
#		r = requests.get(partimage.string)
#	pofn = str(partimagenames.next())
#	with open(pofn, "wb") as code:
#		code.write(r.content)
#	print("saving " + pofn + "from " + filename)
