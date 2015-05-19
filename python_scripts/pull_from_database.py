import mysql.connector
from mysql.connector import MySQL Connection, Error
import getpass 



def get_part_info(pn):
    mysqlpasswd = getpass.getpass('Mysql root password:')
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='PARTDATA',
                                       user='root',
                                       password=mysqlpasswd)
        cursor = conn.cursor()
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor.execute("SELECT * FROM CatalogContentExport WHERE partNumber=%s", (pn,))
            row = cursor.fetchone()
            while row is not None:
                print(row)
                row = cursor.fetchone()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
