#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
import getpass 
import argparse

print("\n\n\nThis script will generate a text file with the name of your choice, consisting of\none part number per line, pulling all part numbers\non a given range of pages from Parts Unlimited catalogs.\nThis can be used in conjunction with the import to bigcommerce script.")

catalogname = raw_input('\n\n\n\n\n\nType a catalog name, exactly as shown.\nYou must choose from the following catalog names\nand be sure to use correct capitalization:\n\nStreet\nFatbook\nATV\nWatercraft\nHelmet_and_Apparel\nSnow\nTire\nOldbook\n\nEnter the catalog you would like to query:')

pagerangelow = raw_input('\n\nGenerate text file with all part numbers from page #: ')

pagerangehigh = raw_input('\n\nTo page #: ')

catalogname = catalogname + "_Current_Year_Page"

sql_command = "SELECT Part_Number FROM PartsUnlimited WHERE " + catalogname + " BETWEEN " + pagerangelow + " AND " + pagerangehigh

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
        cursor.execute(sql_command)     
        print("Pulling all part numbers from " + catalogname + " " + pagerangelow + " to " + catalogname + " " + pagerangehigh)
        row = cursor.fetchone()
        while row is not None:
        #if row is not None:
            print(row[0])
            row = cursor.fetchone()
        else:
            print("That's all the parts in that page range.")
finally:
    cursor.close()
    conn.close()
