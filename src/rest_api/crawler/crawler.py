#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import praw
import unidecode
import logging

logging.basicConfig(filename='logs/rest_api.log', level=logging.DEBUG)


class Crawler:
    def __init__(self, db):
        """
        This method creates a Crawler, assigns a given database to it and a reddit instance
        :param db: RestAPI database to be used
        """
        self.db = db
        self.reddit = praw.Reddit('my_reddit_crawler')

    def retrieve_information(self, subreddit, hot_limit=10):
        """
        This method reads the first n pages (defined by 'hot_limit' parameter) from a
        given subreddit (defined by 'subreddit' parameter) and stores their
        important information in the crawler database.
        :param subreddit: current subreddit
        :param hot_limit: maximum number of pages to fetch
        :return:
        """

        try:
            subreddit = self.reddit.get_subreddit(subreddit)
        except Exception as e:
            print "Error when trying to obtain subreddit information:", e
            raise RuntimeError

        cursor = self.db.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS submissions(submission_title TEXT PRIMARY KEY,
                                                       external_url TEXT,
                                                       discussion_url TEXT,
                                                       submitter TEXT,
                                                       punctuation INTEGER,
                                                       creation_date FLOAT,
                                                       num_comments INTEGER)
                """)
        self.db.commit()

        for submission in subreddit.get_hot(limit=int(hot_limit)):
            cursor.execute('''INSERT OR REPLACE INTO submissions(submission_title,
                                                      external_url,
                                                      discussion_url,
                                                      submitter,
                                                      punctuation,
                                                      creation_date,
                                                      num_comments)
                              VALUES(?,?,?,?,?,?,?)''', (str(unidecode.unidecode(submission.title)),
                                                         str(unidecode.unidecode(submission.permalink)),
                                                         str(unidecode.unidecode(submission.url)),
                                                         str(submission.author),
                                                         submission.score,
                                                         submission.created,
                                                         submission.comments.__len__()))
            self.db.commit()

    def retrieve_total_user_comments_score(self, chosen_subreddit, comments_limit=20):
        """
        This method reads the first 20 pages from a given subreddit
        (defined by 'chosen_subreddit' parameter) and returns that
        information.
        :param chosen_subreddit: current subreddit
        :return: a list of dictionaries with authors and scores
        """
        try:
            subreddit = self.reddit.get_subreddit(chosen_subreddit)
        except Exception as e:
            print "Error when trying to obtain subreddit information:", e
            raise RuntimeError
        comments = {}
        for submission in subreddit.get_hot(limit=comments_limit):
            for comment in submission.comments:
                try:
                    comments[str(comment.author.name)] = comments.get(str(comment.author.name), 0) + comment.score
                except Exception as e:
                    print "Error:", e
        to_return = []
        for author, score in comments.iteritems():
            to_return.append({'author': author, 'score': score})
        return to_return

    def retrieve_user_posts(self, chosen_username, posts_limit=100):
        """
        This method reads the first 100 submissions from a
        given user (defined by 'chosen_username' parameter)
        and returns them.
        :param chosen_username: current username
        :return: a list of dictionaries with submission titles and their subreddits
        """
        user = self.reddit.get_redditor(chosen_username)
        posts = user.get_submitted(limit=posts_limit)
        user_posts = []
        for post in posts:
            user_posts.append({'title': str(unidecode.unidecode(post.title)),
                               'subreddit': str(unidecode.unidecode(post.subreddit.title))})
        return user_posts

    def retrieve_user_comments(self, chosen_username, comments_limit=100):
        """
        This method reads the first 100 comments from a
        given user (defined by 'chosen_username' parameter)
        and returns them.
        :param chosen_username: current username
        :return: a list of dictionaries with comment bodies and their subreddits
        """
        user = self.reddit.get_redditor(chosen_username)
        comments = user.get_comments(limit=comments_limit)
        user_comments = []
        for comment in comments:
            user_comments.append({'comment': str(unidecode.unidecode(comment.body)),
                                  'subreddit': str(unidecode.unidecode(comment.subreddit.title))})
        return user_comments

    def retrieve_user_avg_karma(self, chosen_username, comments_limit=100):
        """
        This method reads the first 100 comments from a
        given user (defined by 'chosen_username' parameter)
        and and calculates the average karma of them.
        :param chosen_username: current username
        :return: a list with a dictionary with the username and the avg karma
        """
        user = self.reddit.get_redditor(chosen_username)
        gen = user.get_comments(limit=comments_limit)
        user_comments = []
        user_karma = 0
        last_ind = 1
        for ind, thing in enumerate(gen):
            user_karma += thing.score
            last_ind = ind
        user_comments.append({'user': chosen_username, 'avg_karma': float(user_karma)/last_ind+1})
        return user_comments
