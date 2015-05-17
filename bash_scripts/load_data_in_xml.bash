#!/bin/bash

for i in ~/parts-unlimited-to-bigcommerce/xmlfiles/*.xml; do mysql PARTDATA -e "LOAD XML INFILE '$i' REPLACE INTO TABLE CatalogContentExport ROWS IDENTIFIED BY '<part>'"; done
