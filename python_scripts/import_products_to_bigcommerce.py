import requests, json, sys
import mysql.connector

##This script was written by Jonah Deinye (paid for with bitcoin!)
##this is the script that creates bigcommerce products. in the current form
##it pulls the product properties and images from the WPS API.
##once I've got the whole Parts Unlimited database mirrored in my mysql database
##and i've got all the images uploaded to my VPS, I will adapt this script to
##create products from the properties and images in my database.
 
## WPS credentials and path
#WPS_URL = 'https://www.wpswebservices.com/version2/wsPRODUCT.pgm'
#DEALER_ID = 'Obscured'
#PASSWORD = 'Obscured'
#DEBUG = True

## Insert the Parts Unlimited mySQL server credentials and path below this line 
connection_object = mysql.connector.connect(user='root', database='partdata')
cursor = connection_object.cursor()

# BigCommerce credentials and URLs
BIG_USER = 'obscured'
BIG_KEY = '60f353d5de97844a3e21052da62a0843'
BIG_API = 'https://store-6o9l9.mybigcommerce.com/api/v2/'
BIG_HEADERS = {'Content-Type': 'application/json'}
BIG_STORE_URL = BIG_API + '%s'
BIG_STORE_PRODUCT_URL = BIG_API + 'products.json'
IMAGE_LOCATION = 'http://www.wpsstatic.com/WPSIMAGES/'
BRAND_IMAGE = 'http://162.243.58.11/comingsoon.jpg'
 
# Script stuff
OVERWRITE = True
 
## Dictionary for converting WPS properties to BigCommerce properties
#conversion_dict = {
#    'iname': 'name',
#    'listprc': 'price',
#    'itmweight': 'weight',
#    #'producttype': 'categories',
## Images will be handled by another script
#    'mainimg': 'mainimg',
#    'longdesc': 'description',
#    'prtnmbr': 'sku',
#    'brand_id': 'brand_id'
#}

## Insert a conversion dictionary below just like the one above but for Parts Unlimited 
conversion_dict = {
    'part_description': 'name',
    'current_suggested_retail': 'price',
    'placeholder': 'weight',

brand_dictionary = {}
 
# Used when testing script
CATNAME = 'testcat'
CATID = '504'
 
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

## For the following section we will need to adapt it to query the mySQL server instead of the WPS API 

def get_part_info(pn):
    #

def get_part_info(pn):
    # Create POST data
    data = {'dealer': DEALER_ID, 'password': PASSWORD, 'prtnmbr': pn, 'output': 'json'}
    
    # Send request
    part_response = requests.post(WPS_URL, data=data)
    
    # Convert JSON response and return docs array
    try:
        response =  part_response.json()
        #if DEBUG:
        #    print response
        return response['response'].get('docs', None)
    
    # If malformed response or error, return None
    except:
        if DEBUG:
            print part_response.text
        return None
 
##the image stuff below will need to be adapted after the image database has been mirrored onto the VPS
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
    
    # Fix description (WPS returns description as an array instead of a string)
    if pd.get('description', None):
        pd['description'] = pd['description'][0]
    
    # Replace category names with category IDs
    #if (pd.get('categories', None)):
    #    for i, cat_name in enumerate(pd['categories']):
    #        cat_id1 = get_category_id(cat_name) 
    #        if not cat_id1:
    #            print 'Creating category %s' % (cat_name,)
    #            cat_id1 = create_category(cat_name)
    #        pd['categories'][i] = cat_id1
 
    
    # Remove mainimg property after setting image_filename
    image_filename = pd.get('mainimg', '')
    if image_filename:
        pd.pop('mainimg')
    
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
 
