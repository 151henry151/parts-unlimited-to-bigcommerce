import sys
import os
import urllib
import bigcommerce
import easywebdav
import mysql.connector

from requests.auth import HTTPDigestAuth
from zipfile import ZipFile
from mysql.connector import Error
from getpass import getpass

# MySQL config
mysqlHost = "localhost"
mysqlDatabase = "PARTDATA"
mysqlUsername = raw_input("Mysql user: ")
mysqlPassword = getpass("Mysql password: ")

# BigCommerce config
bcHost = "store-t0e5k0r.mybigcommerce.com"
bcUser = "henry"
bcToken = "387887eb0156c255e3877871e56c0bf63a22437f"

bcapi = bigcommerce.api.BigcommerceApi(host=bcHost, basic_auth=(bcUser, bcToken))

# BigCommerce webdav config
webdavUrl = "store-t0e5k0r.mybigcommerce.com"
webdavUsername = "151henry151@gmail.com"
webdavPassword = "0d8fa7a8b2f6270c50111a90a95a2beb"

# Brand cache
brand_cache = {}


def getPartsFromFile(file_name):
    f = open(file_name)
    lines = f.readlines()

    parts = []

    for line in lines:
        part = line.rstrip("\n")
        parts.append(part)

    return parts


def getPartFromDB(part_number):
    part = None
    # try to make the connection
    try:
        print "Connecting to mysql..."
        conn = mysql.connector.connect(
            host=mysqlHost,
            database=mysqlDatabase,
            buffered=True,
            user=mysqlUsername,
            password=mysqlPassword)

        cursor = conn.cursor()

        if conn.is_connected():
            print "Getting part %s from db" % part_number
            cursor.execute("SELECT Weight FROM PartsUnlimited WHERE Part_Number=%s", (part_number,))

            row = cursor.fetchone()
            if row:
                partWeight = row[0]
            else:
                partWeight = 0

            cursor.execute("SELECT bullet1, bullet2, bullet3, bullet4, bullet5, bullet6, "
                           "bullet7, bullet8, bullet9, bullet10, bullet11, bullet12, bullet13, "
                           "bullet14, bullet15, bullet16, bullet17, bullet18, bullet19, bullet20, "
                           "bullet21, bullet22, bullet23, bullet24, retailPrice, partImage, productName, "
                           "partDescr, brandName, partImage FROM CatalogContentExport WHERE partNumber=%s",
                           (part_number,))

            row = cursor.fetchone()
            if row:
                description = row[0:23]
                partRetailPrice = row[24]
                partImageLocation = row[25]
                partName = row[26]
                partSubName = row[27]
                partBrandName = row[28]
                partImage = row[29]

                partFullDescription = ". \n".join(x for x in description if x is not None)
                row = cursor.fetchone()

                part = {"name": partName,
                        "price": partRetailPrice,
                        "weight": partWeight,
                        "mainimg": partImageLocation,
                        "description": partFullDescription,
                        "sku": part_number,
                        "brand": partBrandName,
                        "imageZipUrl": partImage}


    except Error as e:
        print e
    finally:
        cursor.close()
        conn.close()

    return part


def uploadImageFromZip(zipUrl, partNumber, productID):
    print "Downloading image for %s" % partNumber
    urllib.urlretrieve(zipUrl, "temp.zip")

    print "Extracting image for %s" % partNumber

    with ZipFile("temp.zip", "r") as z:
        images = z.namelist()
        z.extractall()

    # Connect to webdav
    webdav = easywebdav.connect(webdavUrl, path="dav", auth=HTTPDigestAuth(webdavUsername, webdavPassword),
                                protocol="https")

    print "Uploading images for %s" % partNumber
    for image in images:
        webdav.upload(image, "product_images/import/%s" % image)
        # Create the image
        bcapi.ProductImages.create(productID, image_file=image)

        print "Removing file: %s" % image
        os.remove(image)
    os.remove("temp.zip")


def createProduct(product):
    if not "weight" in product:
        product["weight"] = 0

    if not "availability" in product:
        product["availability"] = "available"

    if not "is_visible" in product:
        product["is_visible"] = True

    if not "type" in product:
        product["type"] = "physical"

    product["brand"] = createBrand(product["brand"])

    print "Creating product %s..." % product["name"]
    try:
        newProduct = bcapi.Products.create(name=product["name"], price=product["price"], weight=product["weight"],
                                           description=product["description"], sku=product["sku"],
                                           categories=product["categories"],
                                           availability=product["availability"], is_visible=product["is_visible"],
                                           type=product["type"])

        productID = newProduct["id"]

        uploadImageFromZip(product["imageZipUrl"], product["sku"], productID)

    except bigcommerce.exception.HttpException as e:
        print e.response.json()[0]["message"]


def createCategory(name):
    print "Creating category %s" % name
    try:
        cat = bcapi.Categories.create(name=name)

        return cat["id"]
    except bigcommerce.exception.HttpException as e:
        error = e.response.json()[0]
        if error["status"] == 409:
            print "Category already exists."
            if "duplicate_category" in error["details"] and error["details"]["duplicate_category"]:
                return error["details"]["duplicate_category"]

        else:
            print "ERROR %i %s" % (error["status"], error["message"])

    return None


def createBrand(name):
    print "Creating brand %s" % name
    if name in brand_cache:
        print "Brand %s already exists" % name
        return brand_cache[name]

    try:
        brand = bcapi.Brands.create(name=name)

        return brand["id"]
    except bigcommerce.exception.HttpException as e:
        error = e.response.json()[0]
        if error["status"] == 409:
            if "duplicate_brand" in error["details"] and error["details"]["duplicate_brand"]:
                print "Brand %s already exists" % name
                return error["details"]["duplicate_brand"]

        else:
            print "ERROR %i %s" % (error["status"], error["message"])

    return None


# Demo part

# part = {"name":"Test",
# 		"price":"100",
# 		"weight":"20",
# 		"mainimg":"",
# 		"categories":[14],
# 		"description":"This is a test object.",
# 		"sku":"1",
# 		"brand": "newBrand"}

def main():
    if len(sys.argv) > 2:
        filename = sys.argv[2]
        category = createCategory(sys.argv[1])
        parts = getPartsFromFile(filename)

        for part in parts:
            partData = getPartFromDB(part)
            partData["categories"] = [category]

            createProduct(partData)


if __name__ == '__main__':
    main()
