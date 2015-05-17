USE PARTDATA
LOAD XML INFILE 'Brand_Catalog_Content_Export(0).xml' 
REPLACE
INTO TABLE CatalogContentExport
ROWS IDENTIFIED BY '<part>'
;
