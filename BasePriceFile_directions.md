**Updating the database:**

* Run 'update_base_header_database.bash', which will 
    1. Run 'basepricefiledownloader.py', which downloads 'BasePriceFile.csv' which is full of part data
    2. Execute a mysql command 'basepricefiledataimport.sql', which updates the PartsUnlimited table with the information in 'BasePriceFile.csv'


**Making the table:**
* Make a script that takes the headers from 'BasePriceFile.csv' and makes a file 'BaseHeaders.csv' (or do it manually)
* Run 'table_init_command_generator.bash' which generates 'table_init_command_.sql' based on the column names found in 'BaseHeaders.csv'
* Execute the 'table_init_command.sql' which creates a table from the headers in BaseHeaders.csv
    

