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

class Crawler:
    def __init__(self, db):
        self.db = db

    def retrieve_information(self, subreddit, hot_limit):
        # This method the first n pages (defined by 'hot_limit' parameter) from a
        # given subreddit (defined by 'subreddit' parameter) and stores their
        # important information in the crawler database.
        reddit = praw.Reddit('bot1')
        try:
            subreddit = reddit.get_subreddit(subreddit)
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
