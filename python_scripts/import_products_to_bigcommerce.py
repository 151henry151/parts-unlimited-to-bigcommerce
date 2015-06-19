#!usr/bin/python

import mysql.connector
import json
import sys
from mysql.connector import Error
import getpass 
import argparse

# Bigcommerce login credentials
BIG_USER = 'obscured'
BIG_KEY = '60f353d5de97844a3e21052da62a0843'
BIG_API = 'https://store-6o9l9.mybigcommerce.com/api/v2/'
BIG_HEADERS = {'Content-Type': 'application/json'}
BIG_STORE_URL = BIG_API + '%s'
BIG_STORE_PRODUCT_URL = BIG_API + 'products.json'
IMAGE_LOCATION = 'http://www.wpsstatic.com/WPSIMAGES/'
BRAND_IMAGE = 'http://162.243.58.11/comingsoon.jpg'

def get_category_id(name):
    get_request = requests.get(BIG_API + 'categories.json', params={'name':name}, headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))
    try:
        cat_list = get_request.json()
        if cat_list:
            return cat_list[0]['id']
        else:
            return None
    except:
        return None
 
def create_category(name):
    rp = requests.post(BIG_API + 'categories.json',
                      data=json.dumps({'name':name}), headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))
    if rp.status_code == 201:
        return rp.json()['id']
    else:
        return get_category_id(name)

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--testing", help="In testing mode, part number 03010101 will be used instead of prompting you to input a part number.", action="store_true")
args = parser.parse_args()
if args.testing:
    print "Testing mode enabled, using part number 03010101"
    pn = "03010101"
else:
    pn = raw_input('Type a single part number with no dashes here to query database:')


def get_part_info(pn):
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

def add_image(image_name, product_id):
    image_data = {'image_file': IMAGE_LOCATION + '%s' % (image_name,)}
    image_info = requests.post(BIG_API + 'products/%s/images.json' % (product_id,),
                               data=json.dumps(image_data), headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))

def create_brand(brand_name):
    if brand_name in brand_dictionary.keys():
        return brand_dictionary[brand_name]
    brand_data = {'name': brand_name, 'image_file': BRAND_IMAGE}
    rp = requests.post(BIG_API + 'brands.json', data=json.dumps(brand_data), headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))
    if rp.status_code == 201:
        print 'Created brand %s' % (brand_name,)
        b_id =  rp.json()['id']
        brand_dictionary[brand_name] = b_id
        return b_id
    else:
        return get_brand_id(brand_name)
 
def get_brand_id(name):
    get_request = requests.get(BIG_API + 'brands.json', params={'name':name}, headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))
    try:
        brand_list = get_request.json()
        if brand_list:
            b_id = brand_list[0]['id']
            brand_dictionary[name] = b_id
            return b_id
        else:
            return None
    except:
        return None
 
def create_item(pd):
    if pd.get('vname', None):
        pd['brand_id'] = create_brand(pd['vname'])
 
    # Swap out compatible keys and remove incompatible keys
    print "Creating item: %s" % (pd['iname'],)
    for k in pd.keys():
        if k in conversion_dict.keys() and k != conversion_dict[k]:
            pd[conversion_dict[k]] = pd[k]
            pd.pop(k)
        elif k not in conversion_dict.values():
            pd.pop(k)
    
    # Add some product properties
    pd['availability'] = 'available'
    pd['is_visible'] = True
    pd['type'] = 'physical'
    pd['categories'] = [CATID,]
    
    if 'weight' not in pd.keys():
        pd['weight'] = 0

 # Create BigCommerce product
    rp = requests.post(BIG_STORE_URL % ('products.json',), data=json.dumps(pd), headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))
    
    # Check for success
    if rp.status_code == 201:
        print "Item %s created" % (pd['name'],)
        if image_filename:
            product_id = rp.json()['id']
            add_image(image_filename, product_id)
    
    elif rp.status_code == 409 and not OVERWRITE:
        print "Cannot continue. Item %s already exists" % (pd['name'],)
    
    elif rp.status_code == 409 and OVERWRITE:
        print "Item %s already exists. Overwriting..." % (pd['name'],)
        existing_product = requests.get(BIG_STORE_PRODUCT_URL, params={'name': pd['name']}, headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))
        existing_product = existing_product.json()
        product_id = existing_product[0]['id']
        requests.delete(BIG_API + 'products/%s.json' % (product_id,),
                        headers = BIG_HEADERS, auth = (BIG_USER, BIG_KEY))
        print 'Deleted item %s' % (pd['name'],)
        rp = requests.post(BIG_STORE_PRODUCT_URL, data=json.dumps(pd), headers = BIG_HEADERS, auth=(BIG_USER, BIG_KEY))
        
        # Get product ID and add image if one exists
        if image_filename:
            product_id = rp.json()['id']
            add_image(image_filename, product_id)
        
        print "Item %s created" % (pd['name'],)
    elif DEBUG:
        print rp.text
        print 'Could not create item %s' % (pd['name'],)
 
if __name__ == '__main__':
    if len(sys.argv) > 2:
        CATNAME = sys.argv[1]
        CATID = create_category(CATNAME)
        
        # Open and read input file
        f = open(sys.argv[2])
        f = f.readlines()
        
        for part_number in f:
            part_number = part_number.rstrip('\n')
            part_info = get_part_info(part_number)
            if part_info:
                for part in part_info:
                    if DEBUG:
                        print "Name: " + part['iname']
                    create_item(part)
    else:
        print 'Correct syntax is import.py categoryname FILE.TXT\nFILE.TXT is a plain text file with a part number on each line'
