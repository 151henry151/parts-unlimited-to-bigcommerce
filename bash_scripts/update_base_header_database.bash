#!/bin/bash

../python_scripts/basepricefiledownloader.py
mysql < ../sql_commands/basepricefilecsvdataimport.sql
