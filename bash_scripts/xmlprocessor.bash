#!/bin/bash

for f in ~/parts-unlimited-to-bigcommerce/catalog_content_xml_files/*.xml; do xmlstarlet c14n < "$f" > ~/parts-unlimited-to-bigcommerce/xmlfiles/"${f##*/}"; done

#for f in ~/github/parts-unlimited-to-bigcommerce/catalog_content_xml_files/*.xml; do xmlstarlet c14n < "$f" > "$f.c14n"; done

#for f in ~/github/parts-unlimited-to-bigcommerce/catalog_content_xml_files/*.xml; do starlet c14n < "$f" > ~/github/parts-unlimited-to-bigcommerce/xmlfiles/"${f##*/}"; done

