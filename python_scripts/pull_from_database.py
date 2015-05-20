#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
import getpass 

mysqlpasswd = getpass.getpass('Mysql root password:')
pn = raw_input('Type a single part number with no dashes in here:')

#mysqlpasswd = "obscured"
#pn = "03010101"

try:
    conn = mysql.connector.connect(host='localhost',
        database='PARTDATA',
        buffered=True,
        user='root',
        password=mysqlpasswd)
    cursor = conn.cursor()
    if conn.is_connected():
        print('Connected to MySQL database')
        cursor.execute("SELECT bullet1, bullet2, bullet3, bullet4, bullet5, bullet6, "
                       "bullet7, bullet8, bullet9, bullet10, bullet11, bullet12, bullet13, "
                       "bullet14, bullet15, bullet16, bullet17, bullet18, bullet19, bullet20, "
                       "bullet21, bullet22, bullet23, bullet24, retailPrice, partImage, productName, "
                       "partDescr FROM CatalogContentExport WHERE partNumber=%s", (pn,))
        row = cursor.fetchone()
        #while row is not None:
        if row is not None:
            print("Pulling Data About Part Number " + pn)
	    tupleOfDescription = row[0:23]
            partSubName = row[27]
            #fullTextOfDescription = bulletPoint.join(tupleOfDescription)
            fullTextOfDescription = ''.join(partSubName, str(tupleOfDescription))
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

print('Here is the data we have about this part:')
print("We have the image location: " + partImageLocation)
print("We have the bullet points for our description: " + fullTextOfDescription)
print("We have the retail price: " + partRetailPrice)
print("We have the part name: " + partName)
print("We have the part sub-name: " + partSubName)
