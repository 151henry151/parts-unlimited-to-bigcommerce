#!/usr/bin/python

# This script will download the image zip files from the data in the brand
# catalog content xml files.
# It needs to be updated to point at the right directories, but also,
# it is no longer going to be used as it is, it will be incorporated into
# the final script, because there are too many image zip files
# to download them all at once, we have to download them one at a time
# as we create bigcommerce products, and delete them locally after they've been
# uploaded to bigcommerce.

from BeautifulSoup import BeautifulSoup
import re
import requests
import itertools

def generator(s1, s2):
	for x in itertools.count():
		yield '%s%s%s' % (s1, x ,s2)
partimagenames = generator("partimage", ".zip")
productimagenames = generator("productimage", ".zip")

for i in range (566):
	filename = "Brand_Catalog_Content_Export(%s).xml" % i
	soup = BeautifulSoup(open(filename))
	
	for partimage in soup.findAll('partimage'):
		if partimage.string != None:
			r = requests.get(partimage.string)
			pofn = str(partimagenames.next())
			with open(pofn, "wb") as code:
				code.write(r.content)
			print("saving " + pofn + "from " + filename)
	for productimage in soup.findAll('productimage'):
		if productimage.string != None:
			r = requests.get(productimage.string)
			profn = str(productimagenames.next())
			with open(profn, "wb") as code:
				code.write(r.content)
			print("saving " + profn + "from " + filename)
