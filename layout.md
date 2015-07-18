Although there are four databases, three of them I don't use and
don't know what are, they were automatically generated

        mysql> show databases;
        +--------------------+
        | Database           |
        +--------------------+
        | information_schema |
        | PARTDATA           |
        | mysql              |
        | performance_schema |
        +--------------------+
        4 rows in set (0.00 sec)

The only one I use is PARTDATA

        mysql> use PARTDATA

In PARTDATA there are two tables

        mysql> show tables;
        +----------------------+
        | Tables_in_PARTDATA   |
        +----------------------+
        | CatalogContentExport |
        | PartsUnlimited       |
        +----------------------+

CatalogContentExport consists of 

*        the baseDealerPrice, 
*       the brandName,
*        24 bullet points about the product which together form the description, 
*        the originalRetailPrice, 
*        the partDescr which is really more of a title than a description,
*        the partImage which is a URL to an image,
*        the partNumber,
*        the partStatusDescr which indicates whether the product is in the current catalogs,
*        the productId which I think is a unique identifier,
*        the productImage which is another image URL,
*        the productName,
*        the punctuatedPartnumber,
*        the retailPrice,
*        any specialInstructions,
*        the supplierNumber, 
*        the uom for Unit Of Measure, 
*        and yourDealerPrice which is what we actually pay

The table is not very well formed, most of the columns are varchar(255), I would like
to rebuild it with better choices for each column.

        mysql> describe CatalogContentExport;
        +----------------------+--------------+------+-----+---------+-------+
        | Field                | Type         | Null | Key | Default | Extra |
        +----------------------+--------------+------+-----+---------+-------+
        | baseDealerPrice      | decimal(6,2) | YES  |     | 0.00    |       |
        | brandName            | varchar(255) | YES  |     | NULL    |       |
        | bullet1              | varchar(255) | YES  |     | NULL    |       |
        | bullet10             | varchar(255) | YES  |     | NULL    |       |
        | bullet11             | varchar(255) | YES  |     | NULL    |       |
        | bullet12             | varchar(255) | YES  |     | NULL    |       |
        | bullet13             | varchar(255) | YES  |     | NULL    |       |
        | bullet14             | varchar(255) | YES  |     | NULL    |       |
        | bullet15             | varchar(255) | YES  |     | NULL    |       |
        | bullet16             | varchar(255) | YES  |     | NULL    |       |
        | bullet17             | varchar(255) | YES  |     | NULL    |       |
        | bullet18             | varchar(255) | YES  |     | NULL    |       |
        | bullet19             | varchar(255) | YES  |     | NULL    |       |
        | bullet2              | varchar(255) | YES  |     | NULL    |       |
        | bullet20             | varchar(255) | YES  |     | NULL    |       |
        | bullet21             | varchar(255) | YES  |     | NULL    |       |
        | bullet22             | varchar(255) | YES  |     | NULL    |       |
        | bullet23             | varchar(255) | YES  |     | NULL    |       |
        | bullet24             | varchar(255) | YES  |     | NULL    |       |
        | bullet3              | varchar(255) | YES  |     | NULL    |       |
        | bullet4              | varchar(255) | YES  |     | NULL    |       |
        | bullet5              | varchar(255) | YES  |     | NULL    |       |
        | bullet6              | varchar(255) | YES  |     | NULL    |       |
        | bullet7              | varchar(255) | YES  |     | NULL    |       |
        | bullet8              | varchar(255) | YES  |     | NULL    |       |
        | bullet9              | varchar(255) | YES  |     | NULL    |       |
        | originalRetailPrice  | decimal(6,2) | YES  |     | 0.00    |       |
        | partDescr            | varchar(255) | YES  |     | NULL    |       |
        | partImage            | varchar(995) | YES  |     | NULL    |       |
        | partNumber           | varchar(255) | YES  |     | NULL    |       |
        | partStatusDescr      | varchar(255) | YES  |     | NULL    |       |
        | productId            | varchar(255) | YES  |     | NULL    |       |
        | productImage         | varchar(255) | YES  |     | NULL    |       |
        | productName          | varchar(255) | YES  |     | NULL    |       |
        | punctuatedPartNumber | varchar(255) | YES  |     | NULL    |       |
        | retailPrice          | varchar(255) | YES  |     | NULL    |       |
        | specialInstructions  | varchar(255) | YES  |     | NULL    |       |
        | supplierNumber       | varchar(255) | YES  |     | NULL    |       |
        | uom                  | varchar(255) | YES  |     | NULL    |       |
        | yourDealerPrice      | decimal(6,2) | YES  |     | 0.00    |       |
        +----------------------+--------------+------+-----+---------+-------+
        40 rows in set (0.01 sec)

That contains most of the data we will need to make a product on bigcommerce. 
However, we have another table, called PartsUnlimited, that has an additional 
105! different fields that can be populated. I won't go through them all as there are
many repeats from the previous table, but essentially, the data this has that the other 
table doesn't is:
        
 *       the availability (and which warehouses have it),
 *       the date the part was added (which may prove useful for updating when new products are added),
 *       whether the part is hazardous or not and whether it can be shipped via air or only ground,
 *       whether the part is trademarked or not,
 *       the advertising policy for the part (which determines whether the part is usable for 
         promotions and sales, because many parts have a minimum advertised price policy which 
         prevents us from putting them on sale online), 
 *       whether the price of the part has changed today or not (which may also prove useful for updating),
 *       the UPC code of the product,
 *       the country of origin,
 *       a "commodity code" that I'm not quite sure what is, but would like to learn about,
 *       the weight of the item, 
 *       whether or not it's considered to be "on close out,"

And then occupying the majority of the table, there are separate columns that indicate whether the 
product was shown and which page (if any) the product was shown on in each catalog, for this
year's catalog and last years catalog. This catalog page data is not all that super exciting,
except that we have the catalogs viewable in a frame on the website, and it may be possible
to design a system where each product will have a link to the relevant page in the relevant
catalog. Most of the information and photos from that page in the catalog are already going 
to be present on the product page, however it would be a cool feature as there sometimes are
better or more photos in the catalog, and there are sometimes (rarely) pieces of information in the
catalogs that are not present anywhere in the product data. It would be a pretty slick feature,
if it's achievable, and the data is all there.

This table is also all varchar(255) and really needs to be rebuilt with more appropriate column types.

        mysql> describe PartsUnlimited;
        +--------------------------------------+--------------+------+-----+---------+-------+
        | Field                                | Type         | Null | Key | Default | Extra |
        +--------------------------------------+--------------+------+-----+---------+-------+
        | Part_Number                          | varchar(255) | YES  |     | NULL    |       |
        | Punctuated_Part_Number               | varchar(255) | YES  |     | NULL    |       |
        | Vendor_Part_Number                   | varchar(255) | YES  |     | NULL    |       |
        | Vendor_Punctuated_Part_Number        | varchar(255) | YES  |     | NULL    |       |
        | Part_Status                          | varchar(255) | YES  |     | NULL    |       |
        | Part_Description                     | varchar(255) | YES  |     | NULL    |       |
        | Original_Retail                      | varchar(255) | YES  |     | NULL    |       |
        | Current_Suggested_Retail             | varchar(255) | YES  |     | NULL    |       |
        | Base_Dealer_Price                    | varchar(255) | YES  |     | NULL    |       |
        | Hazardous_Code                       | varchar(255) | YES  |     | NULL    |       |
        | Truck_Part_Only                      | varchar(255) | YES  |     | NULL    |       |
        | Part_Add_Date                        | varchar(255) | YES  |     | NULL    |       |
        | WI_Availability                      | varchar(255) | YES  |     | NULL    |       |
        | NY_Availability                      | varchar(255) | YES  |     | NULL    |       |
        | TX_Availability                      | varchar(255) | YES  |     | NULL    |       |
        | CA_Availability                      | varchar(255) | YES  |     | NULL    |       |
        | NV_Availability                      | varchar(255) | YES  |     | NULL    |       |
        | NC_Availability                      | varchar(255) | YES  |     | NULL    |       |
        | National_Availability                | varchar(255) | YES  |     | NULL    |       |
        | Trademark                            | varchar(255) | YES  |     | NULL    |       |
        | Ad_Policy                            | varchar(255) | YES  |     | NULL    |       |
        | Price_Changed_Today                  | varchar(255) | YES  |     | NULL    |       |
        | Unit_of_Measure                      | varchar(255) | YES  |     | NULL    |       |
        | UPC_Code                             | varchar(255) | YES  |     | NULL    |       |
        | Brand_Name                           | varchar(255) | YES  |     | NULL    |       |
        | Country_of_Origin                    | varchar(255) | YES  |     | NULL    |       |
        | Commodity_Code                       | varchar(255) | YES  |     | NULL    |       |
        | Product_Code                         | varchar(255) | YES  |     | NULL    |       |
        | Drag_Part                            | varchar(255) | YES  |     | NULL    |       |
        | Weight                               | varchar(255) | YES  |     | NULL    |       |
        | Closeout_Catalog_Indicator           | varchar(255) | YES  |     | NULL    |       |
        | Last_Catalog                         | varchar(255) | YES  |     | NULL    |       |
        | Last_Catalog_Page                    | varchar(255) | YES  |     | NULL    |       |
        | Street_Catalog_Code                  | varchar(255) | YES  |     | NULL    |       |
        | Street_Current_Year                  | varchar(255) | YES  |     | NULL    |       |
        | Street_Current_Year_Page             | varchar(255) | YES  |     | NULL    |       |
        | Street_Last_Year                     | varchar(255) | YES  |     | NULL    |       |
        | Street_Last_Year_Page                | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Catalog_Code                 | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Current_Year                 | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Current_Year_Page            | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Last_Year                    | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Last_Year_Page               | varchar(255) | YES  |     | NULL    |       |
        | ATV_Catalog_Code                     | varchar(255) | YES  |     | NULL    |       |
        | ATV_Current_Year                     | varchar(255) | YES  |     | NULL    |       |
        | ATV_Current_Year_Page                | varchar(255) | YES  |     | NULL    |       |
        | ATV_Last_Year                        | varchar(255) | YES  |     | NULL    |       |
        | ATV_Last_Year_Page                   | varchar(255) | YES  |     | NULL    |       |
        | Offroad_Catalog_Code                 | varchar(255) | YES  |     | NULL    |       |
        | Offroad_Current_Year                 | varchar(255) | YES  |     | NULL    |       |
        | Offroad_Current_Year_Page            | varchar(255) | YES  |     | NULL    |       |
        | Offroad_Last_Year                    | varchar(255) | YES  |     | NULL    |       |
        | Offroad_Last_Year_Page               | varchar(255) | YES  |     | NULL    |       |
        | Snow_Catalog_Code                    | varchar(255) | YES  |     | NULL    |       |
        | Snow_Current_Year                    | varchar(255) | YES  |     | NULL    |       |
        | Snow_Current_Year_Page               | varchar(255) | YES  |     | NULL    |       |
        | Snow_Last_Year                       | varchar(255) | YES  |     | NULL    |       |
        | Snow_Last_Year_Page                  | varchar(255) | YES  |     | NULL    |       |
        | Watercraft_Catalog_Code              | varchar(255) | YES  |     | NULL    |       |
        | Watercraft_Current_Year              | varchar(255) | YES  |     | NULL    |       |
        | Watercraft_Current_Year_Page         | varchar(255) | YES  |     | NULL    |       |
        | Watercraft_Last_Year                 | varchar(255) | YES  |     | NULL    |       |
        | Watercraft_Last_Year_Page            | varchar(255) | YES  |     | NULL    |       |
        | Street_Mid_Year_Catalog_Code         | varchar(255) | YES  |     | NULL    |       |
        | Street_Mid_Year_Current_Year         | varchar(255) | YES  |     | NULL    |       |
        | Street_Mid_Year_Current_Year_Page    | varchar(255) | YES  |     | NULL    |       |
        | Street_Mid_Year_Last_Year            | varchar(255) | YES  |     | NULL    |       |
        | Street_Mid_Year_Last_Year_Page       | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Mid_Year_Catalog_Code        | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Mid_Year_Current_Year        | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Mid_Year_Current_Year_Page   | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Mid_Year_Last_Year           | varchar(255) | YES  |     | NULL    |       |
        | Fatbook_Mid_Year_Last_Year_Page      | varchar(255) | YES  |     | NULL    |       |
        | Helmet_and_Apparel_Catalog_Code      | varchar(255) | YES  |     | NULL    |       |
        | Helmet_and_Apparel_Current_Year      | varchar(255) | YES  |     | NULL    |       |
        | Helmet_and_Apparel_Current_Year_Page | varchar(255) | YES  |     | NULL    |       |
        | Helmet_and_Apparel_Last_Year         | varchar(255) | YES  |     | NULL    |       |
        | Helmet_and_Apparel_Last_Year_Page    | varchar(255) | YES  |     | NULL    |       |
        | Tire_Catalog_Code                    | varchar(255) | YES  |     | NULL    |       |
        | Tire_Current_Year                    | varchar(255) | YES  |     | NULL    |       |
        | Tire_Current_Year_Page               | varchar(255) | YES  |     | NULL    |       |
        | Tire_Last_Year                       | varchar(255) | YES  |     | NULL    |       |
        | Tire_Last_Year_Page                  | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Catalog_Code                 | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Current_Year                 | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Current_Year_Page            | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Last_Year                    | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Last_Year_Page               | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Mid_Year_Catalog_Code        | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Mid_Year_Current_Year        | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Mid_Year_Current_Year_Page   | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Mid_Year_Last_Year           | varchar(255) | YES  |     | NULL    |       |
        | Oldbook_Mid_Year_Last_Year_Page      | varchar(255) | YES  |     | NULL    |       |
        | Future1_Catalog_Code                 | varchar(255) | YES  |     | NULL    |       |
        | Future1_Current_Year                 | varchar(255) | YES  |     | NULL    |       |
        | Future1_Current_Year_Page            | varchar(255) | YES  |     | NULL    |       |
        | Future1_Last_Year                    | varchar(255) | YES  |     | NULL    |       |
        | Future1_Last_Year_Page               | varchar(255) | YES  |     | NULL    |       |
        | Future2_Catalog_Code                 | varchar(255) | YES  |     | NULL    |       |
        | Future2_Current_Year                 | varchar(255) | YES  |     | NULL    |       |
        | Future2_Current_Year_Page            | varchar(255) | YES  |     | NULL    |       |
        | Future2_Last_Year                    | varchar(255) | YES  |     | NULL    |       |
        | Future2_Last_Year_Page               | varchar(255) | YES  |     | NULL    |       |
        | NoShipToCA                           | varchar(255) | YES  |     | NULL    |       |
        | Notes                                | varchar(255) | YES  |     | NULL    |       |
        +--------------------------------------+--------------+------+-----+---------+-------+
        105 rows in set (0.00 sec)

