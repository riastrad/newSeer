#!/usr/bin/env python3
#
# @Author: Josh Erb <josh.erb>
# @Date:   06-Mar-2017 14:03
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 24-Apr-2017 22:04
#
# Code to pull data files down from EC2 instance:
#
# scp -i "Data-Ingester.pem" -r ubuntu@35.165.12.174:~/data/ <destination path>
#
# to function as is, must be run in ~/repos/.aws directory

"""
Quick script to clean up .csv data that was pulled from RSS feeds (ref: eater.py)

Will clean files in place and leave them in the ./data folder - after which the
'dum.py' file will insert all data into a local PostgreSQL database for safekeeping (and storage purposes).
"""

#######################################
#   IMPORTS
#######################################

import os
import ftfy
import pandas as pd
from glob import glob
from tqdm import tqdm
from bs4 import BeautifulSoup


#######################################
#   CONSTANTS
#######################################

data_path = os.path.abspath('data')
data_files = glob(os.path.join(data_path, '*.csv'))

#######################################
#   FUNCTIONS
#######################################

def csv_as_df(file_path):
    """
    Using a file path string as an argument, opens a csv as a dataframe with
    no headers and returns that dataframe.
    """

    with open(file_path, 'r') as f:
        df = pd.read_csv(f, header=None)

    return df

def clean_title(df, col=4):
    """
    A function that takes an RSS feed data frame as its argument and returns a
    dataframe with the regex errors cleaned up as best as can be managed.
    """
    # Quickly iterate over the dataframe and clean each title value
    for i, row in df.iterrows():
        try:    # Encountered problems with data, will need to refactor later
            clean = ftfy.fix_text(df.iloc[i, col])
        except TypeError:
            clean = "Missing Title"

        df.set_value(i, 5, clean)

    return df

def clean_desc(df, col=0):
    """
    A function that takes an RSS feed data frame as its argument and returns a
    dataframe with the html removed from the description column, as best as
    possible given the state of some of the RSS pulls.

    (I'm looking at you, BuzzFeed)
    """

    # similar iteration to clean_title, but leveraging the prebuilt functions that
    # can be run on BeautifulSoup objects to parse html text
    for i, row in df.iterrows():
        try:
            clean = BeautifulSoup(df.iloc[i, col], 'html.parser').text
        except TypeError:
            clean = ""

        df.set_value(i, 6, clean)

    return df

def clean_save(df, file_name, path=data_path):
    """
    Runs the cleaning functions on the text columns of an RSS feed dataframe. A
    file name needs to be provided in order to save properly.

    Note that the final output is saved as a tsv (tab seperated) file in order
    to avoid any unintended consequences with free text commas.
    """
    # add a title name onto the path variable
    new_path = os.path.join(data_path, file_name + '_clean.tsv')

    # run each predefined function on a given data frame
    df = clean_title(df)
    df = clean_desc(df)

    # drop the unneaded, 'dirty' columns (using their indexes)
    df.drop([0,4], axis=1, inplace=True)

    # save the file as a .tsv
    df.to_csv(new_path, sep='\t', header=['pull_ts', 'pubdate', 'publication', 'title', 'description'], index=False)

    return

def main():
    """
    Primary execution function.
    """

    for csv in tqdm(data_files): # the tqdm() function call is only there to show progress, because I imagine running this on a large amount of large files
        name = csv.split('/')[-1][:-4] # using the filename to help generate a new file name
        df = csv_as_df(csv)
        clean_save(df, name)

    return

#######################################
#   EXECUTION
#######################################

if __name__ == '__main__':
    main()
