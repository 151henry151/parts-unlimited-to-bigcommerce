**Rebuilding the database:**

* Run 'update_catalog_content_database.bash', which will 
    1. Delete all the old ZIP files and all the old XML files
    2. Run 'catalog_content_export_zip_downloader.py', which will download all the ZIP files over again, which is against the rules
    3. Run 'catalog_content_export_unzipper.py', which will extract the XML files from the ZIP files,
    4. Run 'xmlprocessor.bash', which will process the XML files to prepare them for import (file encoding stuff I think? I forget)
    5. Run 'load_data_in_xml.bash', which will import the data from the XML files into the CatalogContentExport table


**Updating the database:**

We do not want to download all the ZIP files over again every time we need to update the database, 
because we want to update frequently, and we are not allowed to run 'catalog_content_export_zip_downloader.py'
at all as it currently exists, because it is considered web scraping, and against the terms of our agreement
with the distributor. So, we would like to have a script that does the following:

1. Checks the BasePriceFile table (PartsUnlimited) which is made from CSV data that can be downloaded daily
2. Determines whether there are any new parts in the PartsUnlimited table
3. Determines which brand(s) the new parts are from
4. Downloads only the brand(s) ZIP files which have new products (the ZIPS are sorted by brand, 
   we can use the basic functionality of 'catalog_content_export_zip_downloader.py' but direct it
   to specific brand ZIP files instead of having it download all of them)
5. Unzips the XML files
6. Updates the CatalogContentExport table with the new data
