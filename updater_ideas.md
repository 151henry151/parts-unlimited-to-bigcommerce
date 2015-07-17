**Updating:**

We want to be able to update the final bigcommerce site daily, with current availability and current pricing, and new images if they have changed, and any updates to the descriptions. We will need:

 * A script that checks the WPS API to see if there have been any modifications, for each WPS product in the bigcommerce store
 * A script which completely updates both the Base Price File data and the Catalog Content data for Parts Unlimited in our MYSQL database
    1. Re-download the CSV data completely, wipe out the table and re-build it from the new CSV file
    2. Check in the CSV table and see which parts have been modified or added
    3. Download the necessary ZIP files and update the Catalog Content table
 * A script which then updates each Parts Unlimited product in the bigcommerce store with the most current data from our MYSQL database
