#!/bin/bash

# CAUTION -- This script destroys the Catalog Content Export table and attempts to rebuild it. Do not run this script unless performing significant maintenance and adding columns to the table.
# If you run this script and don't have the Catalog Content Export ZIP files you will need to re-download them all which is very time consuming.

mysql PARTDATA < ~/parts-unlimited-to-bigcommerce/sql_commands/drop_tables.sql 
mysql PARTDATA < ~/parts-unlimited-to-bigcommerce/sql_commands/new_create_table.sql
