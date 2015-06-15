#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
import getpass 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--testing", help="In testing mode, part number 03010101 will be used instead of prompting you to input a part number.", action="store_true")
args = parser.parse_args()
if args.testing:
    print "Testing mode enabled, using part number 03010101"
    pn = "03010101"
else:
    pn = raw_input('Type a single part number with no dashes here to query database:')

mysqlpasswd = getpass.getpass('Mysql server root password:')

try:
    conn = mysql.connector.connect(host='localhost',
        database='PARTDATA',
        buffered=True,
        user='root',
        password=mysqlpasswd)
    cursor = conn.cursor()
    if conn.is_connected():
        print('Connected to MySQL database\n...\n...')
        cursor.execute("SELECT bullet1, bullet2, bullet3, bullet4, bullet5, bullet6, "
                       "bullet7, bullet8, bullet9, bullet10, bullet11, bullet12, bullet13, "
                       "bullet14, bullet15, bullet16, bullet17, bullet18, bullet19, bullet20, "
                       "bullet21, bullet22, bullet23, bullet24, retailPrice, partImage, productName, "
                       "partDescr FROM CatalogContentExport WHERE partNumber=%s", (pn,))
        row = cursor.fetchone()
        #while row is not None:
        if row is not None:
            print("Pulling Data About Part Number " + pn + "\n ... \n ...")
	    tupleOfDescription = row[0:23]
            partSubName = row[27]
            fullTextOfDescription = '. \n'.join(x for x in tupleOfDescription if x is not None)
            partRetailPrice = row[24]
            partImageLocation = row[25]
            partName = row[26]
            row = cursor.fetchone()
            
        else:
            print("No Part Data Found for part number " + pn + " ! Double check the part number or consult with your system administrator (Henry, in this case)")
except Error as e:
    print(e)
finally:
    cursor.close()
    conn.close()

print("The following data was found in our MySQL database for part number " + pn + " and was assigned to various variable names: \n")
print("Image URL: " + partImageLocation + "\n")
print("Description:\n\n -------------- \n\n" + fullTextOfDescription + "\n\n")
print("Current Retail price: " + partRetailPrice + "\n")
print("Part name: " + partName + "\n")
print("Part sub-name: " + partSubName)
