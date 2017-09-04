#!/usr/bin/env python
'''
/***********************************************
*    Title: Songs Platform                     *
*    Author: Guillem Nicolau Alomar Sitjes     *
*    Date: July 23rd, 2017                     *
*    Code version: 0.1                         *
*    Availability: Public                      *
***********************************************/
'''
import argparse
import errno
import os.path
import sqlite3

import web

from crawler.crawler import Crawler


class MyApplication(web.application):
    # This method initializes the web server on a specified hostname and port,
    # and through a web server gateway interface
    def run(self, app_hostname, app_port, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (app_hostname, app_port))


def initialize_db(db_file_name, initialize_data=False):
    # This method checks if the file exists, and if not, tries to create the
    # folder containing it, and a blank file in that path. After that, returns
    # a SQLite database instance linked to that file. 'check_same_thread
    # parameter needs to be set to False to avoid problems between petitions.
    if not os.path.exists(os.path.dirname(db_file_name)):
        try:
            os.makedirs(os.path.dirname(db_file_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if not os.path.isfile(db_file_name) or initialize_data:
        db_file = open(db_file_name, 'w')
    else:
        db_file = open(db_file_name, 'r')
    db_file.close()
    return sqlite3.connect(db_file_name, check_same_thread=False)

# Links between urls and classes
urls = (
    '/fetch_subreddit', 'FetchSubreddit',
    '/get_score_ranking', 'GetScoreRanking',
    '/get_discussion_ranking', 'GetDiscussionRanking',
    '/get_top_users', 'GetTopUsers',
    '/get_karma_stats', 'GetKarmaStats'
)

db = initialize_db('database/data/dbfile.sqlite')


class FetchSubreddit:
    # This method inserts a specified channel_name into the SQLite DB
    def POST(self):
        # Create a Crawler
        my_crawler = Crawler(db)
        # Make it save the data about the first n pages of a given subreddit into our database
        my_crawler.retrieve_information(web.input().chosen_subreddit, web.input().num_pages)


class GetScoreRanking:
    # This method inserts a specified performer_name into the SQLite DB
    def GET(self):
        pass


class GetDiscussionRanking:
    # This method inserts a specified song name and performer into the SQLite DB
    def GET(self):
        pass


class GetTopUsers:
    # This method inserts a specified play into the SQLite DB
    def GET(self):
        pass


class GetKarmaStats:
    # This method retrieves all songs from a specified channel that were
    # reproduced during a specified period of time.
    def GET(self):
        pass



if __name__ == "__main__":
    # Arguments are taken from command line
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-H', action="store", dest="hostname",
                        default="localhost", type=str)
    parser.add_argument('-P', action="store", dest="port",
                        default=8080, type=int)
    args = parser.parse_args()

    hostname = args.hostname
    port = args.port

    # An instance of the server is created
    app = MyApplication(urls, globals())
    # and run
    app.run(hostname, port)