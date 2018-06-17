#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import argparse
import sqlite3
import json
import logging
import web
from database.database import Database
from crawler.crawler import Crawler
from src.settings import rest_api_log
from src.settings import database_file

logging.basicConfig(filename=rest_api_log, level=logging.DEBUG)


class MyApplication(web.application):
    def run(self, server_hostname, server_port, *middleware):
        """
        This method initializes the web server on a specified hostname and port,
        and through a web server gateway interface
        :param server_hostname: hostname where the server will be located
        :param server_port: port that the server will use
        :param middleware: .
        :return: server running
        """
        logging.debug('Rest API started with parameters:' +
                      str(server_hostname) + ", " +
                      str(server_port))
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (server_hostname, server_port))


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

db = Database.initialize_db(database_file)


class FetchSubreddit:
    @staticmethod
    def POST():
        """
        This method fetches the needed information from Reddit.com in order to
        run modes 1 (GetScoreRanking) and 2 (GetDiscussionRanking)
        and persists it into the SQLite DB
        :return:
        """
        my_input = web.input(chosen_subreddit='python', num_pages=100)
        my_db = Database.initialize_db(database_file)
        logging.debug('FetchSubreddit method called with parameters:' +
                      str(my_input.chosen_subreddit) + ", " +
                      str(my_input.num_pages))
        try:
            subreddit = my_input.chosen_subreddit
            num_pages = my_input.num_pages
        except Exception as e:
            logging.error("Error in FetchSubreddit. " +
                          "Not all parameters where given, or their format is incorrect." + str(e))
        my_crawler = Crawler(my_db)
        my_crawler.retrieve_information(subreddit, num_pages)
        del my_crawler


class GetScoreRanking:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the score
        ranking from the SQLite DB and returns it to the main application.
        :return: data needed to create the Score Ranking
        """
        logging.debug('GetScoreRanking method called')
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submission_title, punctuation, discussion_url FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append('GetScoreRanking error:' + str(e))
            logging.error('GetScoreRanking error:' + str(e))
        if len(errors) == 0:
            for page in pages:
                result.append({'title': page[0],
                               'score': page[1],
                               'url': page[2]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetDiscussionRanking:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the discussion
        ranking from the SQLite DB and returns it to the main application.
        :return: data needed to create the Discussion Ranking
        """
        logging.debug('GetDiscussionRanking method called')
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submission_title, num_comments, discussion_url FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append('GetDiscussionRanking error:' + str(e))
            logging.error('GetDiscussionRanking error:' + str(e))
        if len(errors) == 0:
            for page in pages:
                result.append({'title': page[0],
                               'num_comments': page[1],
                               'url': page[2]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetTopUsersSubmissionsScore:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the ranking of
        top users by submission score from the SQLite DB and returns it to
        the main application.
        :return: data needed to create the Ranking of top users by submission score
        """
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submitter, punctuation, submission_title FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append('GetTopUsersSubmissionsScore error:' + str(e))
            logging.error('GetTopUsersSubmissionsScore error:' + str(e))
        if len(errors) == 0:
            for page in pages:
                result.append({'submitter': page[0],
                               'punctuation': page[1],
                               'submission_title': page[2]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetTopUsersSubmissionsNum:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the ranking of
        top users by submissions from the SQLite DB and returns it to
        the main application.
        :return: data needed to create the Ranking of top users by submissions
        """
        errors = []
        result = []
        cursor = db.cursor()
        try:
            cursor.execute('''SELECT submitter, submission_title FROM submissions''')
            pages = cursor.fetchall()
        except sqlite3.OperationalError as e:
            errors.append('GetTopUsersSubmissionsNum error:' + str(e))
            logging.error('GetTopUsersSubmissionsNum error:' + str(e))
        if len(errors) == 0:
            for page in pages:
                result.append({'submitter': page[0],
                               'submission_title': page[1]})
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetTopUsersCommentsScore:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the ranking of
        top users by submissions from Reddit.com and returns it to the main
        application.
        :return: data needed to create the Ranking of top users by comments score
        """
        logging.debug('GetTopUsersCommentsScore method called')
        my_input = web.input(chosen_subreddit='Python')
        errors = []
        try:
            chosen_subreddit = my_input.chosen_subreddit
        except Exception as e:
            errors.append('GetTopUsersCommentsScore error:' + str(e))
            logging.error('GetTopUsersCommentsScore error:' + str(e))
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_total_user_comments_score(chosen_subreddit)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetPostsByUser:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the list
        of submissions by user from Reddit.com and returns it to the main
        application.
        :return: data needed to create the list of submissions by user
        """
        logging.debug('GetPostsByUser method called')
        my_input = web.input(chosen_username='guillemnicolau')
        errors = []
        try:
            chosen_username = my_input.chosen_username
        except Exception as e:
            errors.append('GetPostsByUser error:' + str(e))
            logging.error('GetPostsByUser error:' + str(e))
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_user_posts(chosen_username)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetCommentsByUser:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the list
        of comments by user from Reddit.com and returns it to the main
        application.
        :return: data needed to create the list of comments by user
        """
        logging.debug('GetCommentsByUser method called')
        my_input = web.input(chosen_username='guillemnicolau')
        errors = []
        try:
            chosen_username = my_input.chosen_username
        except Exception as e:
            errors.append('GetCommentsByUser error:' + str(e))
            logging.error('GetCommentsByUser error:' + str(e))
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_user_comments(chosen_username)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


class GetKarmaStats:
    @staticmethod
    def GET():
        """
        This method fetches the information needed to create the statistic
        of average comment karma by user from Reddit.com and returns it to the main
        application.
        :return: data needed to calculate the average comment karma by user
        """
        logging.debug('GetKarmaStats method called')
        my_input = web.input(chosen_username='guillemnicolau')
        errors = []
        try:
            chosen_username = my_input.chosen_username
        except Exception as e:
            errors.append('GetKarmaStats error:' + str(e))
            logging.error('GetKarmaStats error:' + str(e))
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_user_avg_karma(chosen_username)
        del my_crawler
        if len(errors) == 0:
            return json.dumps({'result': result, 'code': 0})
        else:
            return json.dumps({'result': result, 'code': len(errors), 'errors': list(errors)})


if __name__ == "__main__":
    # Arguments are taken from command line
    parser = argparse.ArgumentParser(description='Reddit Crawler Server', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--hostname', action="store", dest="hostname",
                        help="Hostname of the server",
                        default="localhost", type=str)
    parser.add_argument('--port', action="store", dest="port",
                        help="Port of the server",
                        default=8080, type=int)

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port

    # An instance of the server is created
    app = MyApplication(urls, globals())
    # and run
    app.run(hostname, port)
