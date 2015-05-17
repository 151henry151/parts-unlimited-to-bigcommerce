#!/bin/bash
~/parts-unlimited-to-bigcommerce/python_scripts/catalog_content_export_zip_downloader.py
~/parts-unlimited-to-bigcommerce/python_scripts/catalog_content_export_unzipper.py
~/parts-unlimited-to-bigcommerce/bash_scripts/xmlprocessor.bash
echo "processing XML files ..."
echo "Done."
~/parts-unlimited-to-bigcommerce/bash_scripts/load_data_in_xml.bash
echo "Updating mySQL database..."
echo "Done."
