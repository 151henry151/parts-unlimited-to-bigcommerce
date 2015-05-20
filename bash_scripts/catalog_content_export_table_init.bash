#!/bin/bash
mysql PARTDATA < ~/parts-unlimited-to-bigcommerce/sql_commands/drop_tables.sql 
mysql PARTDATA < ~/parts-unlimited-to-bigcommerce/sql_commands/new_create_table.sql
