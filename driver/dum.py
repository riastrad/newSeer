#!/usr/bin/env python3
#
# @Author: Josh Erb <josh.erb>
# @Date:   06-Mar-2017 15:03
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 13-Apr-2017 14:04

"""
Quick script to glob up a bunch of tsv files and insert them into a local
PostgreSQL instance using psycopg2.

Will only work if files have been previously cleaned using the cleaner.py script
once this is completed and results have been validated, feel free to delete
raw .csv files.
"""

#######################################
#   IMPORTS
#######################################

import psycopg2
import pandas as pd
from cleaner import csv_as_df

#######################################
#   CONSTANTS
#######################################

data_path = os.path.abspath('data')
data_files = glob(os.path.join(data_path, '*.tsv'))

#######################################
#   FUNCTIONS
#######################################

def insert_data(df, conn):
    """
    Uses pandas and psycopg2 to insert a dataframe into a pre-existing SQL
    database table on a local PostgreSQL instance.

    Note that a connection must have been opened and passed to this function in
    order for it to run correctly.
    """
    pass

def main():
    """
    Primary execution function.
    """
    # initialize the db connection & cursor
    conn = psycopg2.connect("dbname=seer user=josh.erb")
    cur = conn.cursor()

    # add manipulation code here
    for data in data_files:
        # right here

    # close out connection
    cur.close()
    conn.close()

    return

#######################################
#   EXECUTION
#######################################

if __name__ == '__main__':
    main()
