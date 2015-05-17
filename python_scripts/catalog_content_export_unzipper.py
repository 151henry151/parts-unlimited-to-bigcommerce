#!/usr/bin/python
# this script unzips the brand catalog content export zip files
# one at a time, and numbers each exported xml file

import zipfile
import shutil
import os
import glob

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
output_directory = "../catalog_content_xml_files"

if os.path.isdir(working_directory):
	os.chdir(working_directory)
	print("Changing working directory to " + working_directory + " ...")
	cont = True
else:
	cont = bool_str(raw_input("Could not change working directory. Continue? (y/n):"))
if cont:
	if os.path.isdir(output_directory):
		print("Setting output directory to " + output_directory + " ...")
		doproceed = True
	else:
		doproceed = bool_str(raw_input("Could not set ouput directory to " + output_directory + " ... Double check to see if it exists. Do you wish to proceed using current working directory for output? (y/n):"))
	
	if  doproceed:
		for i in glob.glob('*.zip'):
			#filename = "Brand_Catalog_Content_Export(%s).zip" % i
			zf = zipfile.ZipFile(i)
			print("Extracting " + i + " ...")
			zf.extractall()
			shutil.move("Brand_Catalog_Content_Export.xml", "../catalog_content_xml_files/%s.xml" % i)
			print("Moving " + i + " to ~/parts-unlimited-to-bigcommerce/catalog_content_xml_files/" + i + ".xml")
