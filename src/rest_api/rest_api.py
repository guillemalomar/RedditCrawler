#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import argparse
# import errno
# import os.path
import sqlite3
import json

import web
from database.database import Database
from crawler.crawler import Crawler


class MyApplication(web.application):
    # This method initializes the web server on a specified hostname and port,
    # and through a web server gateway interface
    def run(self, app_hostname, app_port, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (app_hostname, app_port))

# Links between urls and classes
urls = (
    '/fetch_subreddit', 'FetchSubreddit',
    '/get_score_ranking', 'GetScoreRanking',
    '/get_discussion_ranking', 'GetDiscussionRanking',
    '/get_top_users', 'GetTopUsers',
    '/get_karma_stats', 'GetKarmaStats'
)

db = Database.initialize_db('database/data/dbfile.sqlite')


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
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submission_title, punctuation FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append(str(e) + ". To load test data, run the application with option '--add-data")
        if len(errors) == 0:
            for page in pages:
                result.append({'title': page[0],
                               'score': page[1]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetDiscussionRanking:
    # This method inserts a specified song name and performer into the SQLite DB
    def GET(self):
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submission_title, num_comments FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append(str(e) + ". To load test data, run the application with option '--add-data")
        if len(errors) == 0:
            for page in pages:
                result.append({'title': page[0],
                               'num_comments': page[1]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


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
