#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
import getpass 

mysqlpasswd = getpass.getpass('Mysql root password:')

# Use raw_input pn for final version, use pn = "" for testing purposes
#pn = "03010101"

try:
    conn = mysql.connector.connect(host='localhost',
        database='PARTDATA',
        buffered=True,
        user='root',
        password=mysqlpasswd)
    cursor = conn.cursor()
    if conn.is_connected():
        print('Connected to MySQL database\n...\n...')
        pn = raw_input('Type a single part number with no dashes here to query database:')
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
            #fullTextOfDescription = bulletPoint.join(tupleOfDescription)
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

print("Data in our MySQL database for part number " + pn + ": \n")
print("Image URL: " + partImageLocation + "\n")
print("Description: " + fullTextOfDescription + "\n\n")
print("Current Retail price: " + partRetailPrice + "\n")
print("Part name: " + partName + "\n")
print("Part sub-name: " + partSubName)
