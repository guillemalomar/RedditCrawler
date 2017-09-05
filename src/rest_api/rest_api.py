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
import logging
import web
from database.database import Database
from crawler.crawler import Crawler

logging.basicConfig(filename='rest_api.log', level=logging.DEBUG)


class MyApplication(web.application):
    # This method initializes the web server on a specified hostname and port,
    # and through a web server gateway interface
    def run(self, app_hostname, app_port, *middleware):
        logging.debug('Rest API started with parameters:' +
                      str(app_hostname) + ", " +
                      str(app_port))
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (app_hostname, app_port))

# Links between urls and classes
urls = (
    '/fetch_subreddit', 'FetchSubreddit',
    '/get_score_ranking', 'GetScoreRanking',
    '/get_discussion_ranking', 'GetDiscussionRanking',
    '/get_top_users_by_submissions_score', 'GetTopUsersSubmissionsScore',
    '/get_top_users_by_submissions', 'GetTopUsersSubmissionsNum',
    '/get_top_users_by_comments_score', 'GetTopUsersCommentsScore',
    '/get_posts_by_user', 'GetPostsByUser',
    '/get_comments_by_user', 'GetCommentsByUser',
    '/get_karma_stats', 'GetKarmaStats'
)

db = Database.initialize_db('database/data/dbfile.sqlite')


class FetchSubreddit:
    # This method inserts a specified channel_name into the SQLite DB
    def POST(self):
        db = Database.initialize_db('database/data/dbfile.sqlite')
        logging.debug('FetchSubreddit method called with parameters:' +
                      str(web.input().chosen_subreddit) + ", " +
                      str(web.input().num_pages))
        errors = []
        try:
            subreddit = web.input().chosen_subreddit
            num_pages = web.input().num_pages
        except Exception as e:
            errors.append(str(e) + ". Not all parameters where given, or their format is incorrect.")
        # Create a Crawler
        my_crawler = Crawler(db)
        # Make it save the data about the first n pages of a given subreddit into our database
        my_crawler.retrieve_information(subreddit, num_pages)
        del my_crawler


class GetScoreRanking:
    # This method inserts a specified performer_name into the SQLite DB
    def GET(self):
        logging.debug('GetScoreRanking method called')
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submission_title, punctuation, discussion_url FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append(str(e) + ". To load test data, run the application with option '--add-data")
        if len(errors) == 0:
            for page in pages:
                result.append({'title': page[0],
                               'score': page[1],
                               'url': page[2]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetDiscussionRanking:
    # This method inserts a specified song name and performer into the SQLite DB
    def GET(self):
        logging.debug('GetDiscussionRanking method called')
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submission_title, num_comments, discussion_url FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append(str(e) + ". To load test data, run the application with option '--add-data")
        if len(errors) == 0:
            for page in pages:
                result.append({'title': page[0],
                               'num_comments': page[1],
                               'url': page[2]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetTopUsersSubmissionsScore:
    # This method inserts a specified play into the SQLite DB
    def GET(self):
        logging.debug('GetTopUsersSubmissionsScore method called')
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submitter, punctuation, submission_title FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append(str(e) + ". To load test data, run the application with option '--add-data")
        if len(errors) == 0:
            for page in pages:
                result.append({'submitter': page[0],
                               'punctuation': page[1],
                               'submission_title': page[2]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetTopUsersSubmissionsNum:
    # This method inserts a specified play into the SQLite DB
    def GET(self):
        logging.debug('GetTopUsersSubmissionsNum method called')
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submitter, submission_title FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append(str(e) + ". To load test data, run the application with option '--add-data")
        if len(errors) == 0:
            for page in pages:
                result.append({'submitter': page[0],
                               'submission_title': page[1]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetTopUsersCommentsScore:
    # This method inserts a specified play into the SQLite DB
    def GET(self):
        logging.debug('GetTopUsersCommentsScore method called')
        errors = []
        try:
            chosen_subreddit = web.input().chosen_subreddit
        except Exception as e:
            errors.append(str(e) + ". Not all parameters where given, or their format is incorrect.")
        # Create a Crawler
        my_crawler = Crawler(db)
        # Make it search for the top users in the subreddit, ordered by comments score
        result = my_crawler.retrieve_total_user_comments_score(chosen_subreddit)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetPostsByUser:
    # This method inserts a specified play into the SQLite DB
    def GET(self):
        logging.debug('GetPostsByUser method called')
        errors = []
        try:
            chosen_username = web.input().chosen_username
        except Exception as e:
            errors.append(str(e) + ". Not all parameters where given, or their format is incorrect.")
        # Create a Crawler
        my_crawler = Crawler(db)
        # Make it search for the top users in the subreddit, ordered by comments score
        result = my_crawler.retrieve_user_posts(chosen_username)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetCommentsByUser:
    # This method inserts a specified play into the SQLite DB
    def GET(self):
        logging.debug('GetCommentsByUser method called')
        errors = []
        try:
            chosen_username = web.input().chosen_username
        except Exception as e:
            errors.append(str(e) + ". Not all parameters where given, or their format is incorrect.")
        # Create a Crawler
        my_crawler = Crawler(db)
        # Make it search for the top users in the subreddit, ordered by comments score
        result = my_crawler.retrieve_user_comments(chosen_username)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetKarmaStats:
    # This method retrieves all songs from a specified channel that were
    # reproduced during a specified period of time.
    def GET(self):
        logging.debug('GetKarmaStats method called')
        errors = []
        try:
            chosen_username = web.input().chosen_username
        except Exception as e:
            errors.append(str(e) + ". Not all parameters where given, or their format is incorrect.")
        # Create a Crawler
        my_crawler = Crawler(db)
        # Make it search for the top users in the subreddit, ordered by comments score
        result = my_crawler.retrieve_user_avg_karma(chosen_username)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


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
