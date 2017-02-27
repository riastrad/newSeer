#!/usr/bin/env python3
#
# @Author: Josh Erb <josh.erb>
# @Date:   27-Feb-2017 11:02
# @Email:  josh.erb@excella.com
# @Last modified by:   josh.erb
# @Last modified time: 27-Feb-2017 11:02

"""
Main driver script for ingesting RSS data. Uses the ArticleFeed() object
from the feeder.py script and a dictionary of publications and RSS urls in order
to save data into a daily .csv file.
"""

#######################################
#   IMPORTS
#######################################
import os
from datetime import datetime
from feeder import ArticleFeed

#######################################
#   CONSTANTS
#######################################

feeds = {
    'New York Times': 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'BuzzFeed': 'https://www.buzzfeed.com/usnews.xml',
    'Slate': 'http://feeds.slate.com/slate',
    'The New Yorker': 'http://www.newyorker.com/feed/news',
    'Wall Street Journal': 'http://www.wsj.com/xml/rss/3_7085.xml',
#    'Washington Post': 'http://feeds.washingtonpost.com/rss/national',
    'The Daily Beast': 'http://feeds.feedburner.com/thedailybeast/articles?format=xml',
}

#######################################
#   FUNCTIONS
#######################################

def iterate_feeds(feed_list, time=datetime.utcnow().date()):
    """
    A function to loop over feeds contained in a dictionary object. Expects that
    object is formatted with [key]:[value] consistent with [publication name]:[RSS Feed URL]
    """
    # Point functions to save data in folder in the current working directory
    path = os.path.abspath('data/feed_data_' + str(time) + '.csv')

    # Iterate through the dictionary and grab the article data for all feeds
    for key, value in feed_list.items():
        rss = ArticleFeed(key)
        rss.get(value)
        rss.dump(path)

    return

def main():
    """
    Primary execution function
    """
    # Run our iterator and generate our feed objects
    iterate_feeds(feeds)

    return

#######################################
#   EXECUTION
#######################################

if __name__ == '__main__':
    main()
