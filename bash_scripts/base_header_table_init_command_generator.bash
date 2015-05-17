#!/bin/bash

# this bash script creates an SQL command and saves it to table.sql
# the sql command makes a MYSQL table BaseHeaders
# from the file called BaseHeaders.csv in the current
# working directory

IFS=, read -r -a array < BaseHeaders.csv
array=("${array[@]//[ -]/_}")
#the following replacement line did indeed replace all dashes with underscores but also replaced all underscores with spaces
#array=("${array[@]//-/_}")
{
  echo 'CREATE TABLE BaseHeaders ('
  for field in "${array[@]}"; do
    printf "\t%s\t\tVARCHAR(255),\n" "$field";
#to enclose column names in backticks, add backticks around the %s as shown below
#printf "\t'%s'\tVARCHAR(255),\n"
  done
  echo ');'
} > baseheadertable.sql 
