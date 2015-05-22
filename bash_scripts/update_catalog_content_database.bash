#!/bin/bash

# The first command in this script has been commented out to avoid infringing on Parts Unlimited's policy on web scraping.
# It may be permissible to download individual zip files if they add new brands, but downloading all their zip files at once is clearly a violation of the agreement, so don't uncomment it


#~/parts-unlimited-to-bigcommerce/python_scripts/catalog_content_export_zip_downloader.py
~/parts-unlimited-to-bigcommerce/python_scripts/catalog_content_export_unzipper.py
~/parts-unlimited-to-bigcommerce/bash_scripts/xmlprocessor.bash
echo "processing XML files ..."
echo "Done."
~/parts-unlimited-to-bigcommerce/bash_scripts/load_data_in_xml.bash
echo "Updating mySQL database..."
echo "Done."
