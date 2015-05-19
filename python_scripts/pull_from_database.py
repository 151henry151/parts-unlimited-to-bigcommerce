#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
import getpass 

mysqlpasswd = getpass.getpass('Mysql root password:')
pn = raw_input('Type a single part number with no dashes in here:')
try:
    conn = mysql.connector.connect(host='localhost',
        database='PARTDATA',
        user='root',
        password=mysqlpasswd)
    cursor = conn.cursor()
    if conn.is_connected():
        print('Connected to MySQL database')
        cursor.execute("SELECT partImage FROM CatalogContentExport WHERE partNumber=%s", (pn,))
        row = cursor.fetchone()
        while row is not None:
            print('Assigning image location')
            partImageLocation = row[0]
            row = cursor.fetchone()
        cursor.execute("SELECT retailPrice FROM CatalogContentExport WHERE partNumber=%s", (pn,))
        row = cursor.fetchone()
        while row is not None:
            print('Assigning retail price')
            partRetailPrice = row[0]
            row = cursor.fetchone()
        cursor.execute("SELECT bullet1 FROM CatalogContentExport WHERE partNumber=%s", (pn,))
        row = cursor.fetchone()
        while row is not None:
            print('Creating description from bulletpoints')
            fullTextOfDescription = row[0]
            row = cursor.fetchone()
except Error as e:
    print(e)
finally:
    cursor.close()
    conn.close()

print('Here is the data we have about this part:')
print("We have the image location: " + partImageLocation)
print("We have the bullet points for our description: " + fullTextOfDescription)
print("We have the retail price: " + partRetailPrice)

