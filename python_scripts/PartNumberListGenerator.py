#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
import getpass 
import argparse

print("\n\n\nThis script will generate a text file with the name of your choice, consisting of\none part number per line, pulling all part numbers\non a given range of pages from Parts Unlimited catalogs.\nThis can be used in conjunction with the import to bigcommerce script.")

catalogname = raw_input('\n\n\n\n\n\nType a catalog name, exactly as shown.\nYou must choose from the following catalog names\nand be sure to use correct capitalization:\n\nStreet_Current_Year\nFatbook_Current_Year\nATV_Current_Year\nWatercraft_Current_Year\nHelmet_and_Apparel_Current_Year\nSnow_Current_Year\nTire_Current_Year\nOldbook_Current_Year\n\nEnter the catalog you would like to query:')

pagerangelow = raw_input('\n\nGenerate text file with all part numbers from page #: ')

pagerangehigh = raw_input('\n\nTo page #: ')

catalogname = catalogname + "_Page"

mysqlpasswd = getpass.getpass('\n\nMysql server root password:')

try:
    conn = mysql.connector.connect(host='localhost',
        database='PARTDATA',
        buffered=True,
        user='root',
        password=mysqlpasswd)
    cursor = conn.cursor()
    if conn.is_connected():
        print('\n\nConnected to MySQL database\n...\n...')
        cursor.execute("SELECT Part_Number FROM PartsUnlimited WHERE %s BETWEEN %s AND %s"(catalogname,pagerangelow,pagerangehigh,))     
        print("Pulling all part numbers from pages numbered between " + pagerangelow + "\n ..." + pagerangehigh + " \n ..." + "\n in catalog " + catalogname)
        row = cursor.fetchone()
        #while row is not None:
        if row is not None:
            print(Part_Number)
        else:
            print("That's all the parts in that page range.")
finally:
    cursor.close()
    conn.close()
