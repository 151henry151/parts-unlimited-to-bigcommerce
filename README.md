

Parts Unlimited to Bigcommerce

A project to automate the creation of Bigcommerce products from the Parts Unlimited database

The ultimate goal being to have a single script that you can run with part numbers for input that will create Bigcommerce products complete with images, descriptions, prices, etc.

There are two ways that Parts Unlimited provides us with data. Some of their data is available in a CSV file called BasePriceFile.csv. The rest of their data is available to us only as a collection of ZIP files that contain XML files full of data.

We will refer to those two sources of data as the Base Price File Data and the Catalog Content Data. We need both, because one contains the current up-to-date pricing, and the other contains the images. They both contain other data as well, with a little bit of overlap, but you need to get both in order to get all the data available to us.

**Usage**

The Base Price File Data Transfer will update the PartsUnlimited table in the PARTDATA mySQL database.

The Catalog Content Data Transfer will update the CatalogContentExport table in the PARTDATA mySQL database. This functionality is not yet ready for use. DO NOT attempt to run the Catalog Content Data Transfer until all web-scraping functionality has been eliminated or we may inadvertently violate the terms of our agreement with Parts Unlimited.

  * Base Price File Data Transfer:
     * Execute update_base_header_database.bash
  * Catalog Content Data Transfer:
     * Execute update_catalog_content_database.bash -- NOT YET READY FOR USE

**Components of Base Price File Data Transfer:**

  * 'basepricefiledownloader.py' -- downloads 'BasePriceFile.csv' which is full of part data
  * 'BaseHeaders.csv' -- is made from BasePriceFile.csv (need to finalize script that does this)
  * 'table_init_command_generator.bash' -- creates 'table_init_command_.sql'
  * 'table_init_command.sql' -- creates a table from the headers in BaseHeaders.csv
  * 'basepricefilecsvdataimport.sql' -- loads the data from BasePriceFile.csv into a MySQL table that  'table_init_command.sql' created

**Components of Catalog Content Data Transfer:**

  * 'catalog_content_export_zip_downloader.py' -- downloads the catalog content ZIP files -- This is the portion that incorporates web-scraping and needs to be modified to avoid violation of our agreements.
  * 'catalog_content_export_unzipper.py' -- Extracts the XML files from the catalog content ZIP files
  * 'xmlprocessor.bash' -- Processes the XML files to prepare them for import
  * 'load_data_in_xml.bash' -- Imports the data from the XML files to our mySQL database
  * 'update_database.bash' -- Runs all of the other scripts in the XML program -- Has been temporarily modified to skip catalog_content_export_zip_downloader.py

