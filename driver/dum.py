#!/usr/bin/env python3
#
# @Author: Josh Erb <josh.erb>
# @Date:   06-Mar-2017 15:03
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 24-Apr-2017 22:04

"""
Quick script to glob up a bunch of tsv files and insert them into a local
sqlite3 database.

Will only work if files have been previously cleaned using the cleaner.py
script once this is completed and results have been validated, feel free to
delete raw .csv files.
"""

#######################################
#   IMPORTS
#######################################

import os
import sqlite3
import pandas as pd
from tqdm import tqdm
from glob import glob

#######################################
#   CONSTANTS
#######################################

data_path = os.path.abspath('data')
data_files = glob(os.path.join(data_path, '*.tsv'))

#######################################
#   FUNCTIONS
#######################################


def insert_data(file_list=data_files):
    """
    Uses pandas and sqlite to insert a dataframe into your local database.

    Note that a connection must have been opened and passed to this function in
    order for it to run correctly.
    """
    # initialize the db connection & cursor
    conn = sqlite3.connect(os.path.join(data_path, 'news.db'))

    # add manipulation code here
    # (tqdm call used to indicate progress in CLI)
    for data in tqdm(file_list, desc='Dumping Progress'):
        # load file into df object
        df = pd.read_csv(data, sep='\t')
        # use the connection to insert the df into our db table
        df.to_sql('news', conn, if_exists='append')
        # Save changes (necessary?)
        conn.commit()

    # close out connection
    conn.close()


def drop_data():
    """
    Quick function to glob the .csv files and remove them quickly. Might not
    use this one for a while...just to make sure nothing is
    wrong with data cleaning.
    """
    files = glob(os.path.join(data_path, '*.csv'))

    # iterate over all the .csv files and drop each one
    for data in files:
        os.remove(data)


def main():
    """
    Primary execution function.
    """
    insert_data()


#######################################
#   EXECUTION
#######################################

if __name__ == '__main__':
    main()
