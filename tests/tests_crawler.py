import unittest
from crawler.crawler import Crawler
from database.database import Database
import os
import praw


class Crawler_Tests(unittest.TestCase):

    def test_init(self):
        db = Database.initialize_db('data/dbfile.sqlite')
        my_crawler = Crawler(db)
        self.assertEquals(db, my_crawler.db)
        self.assertEquals(praw.Reddit, type(my_crawler.reddit))

    def test_retrieveinfo(self):
        try:
            os.remove('data/dbfile.sqlite')
        except OSError:
            pass
        db = Database.initialize_db('data/dbfile.sqlite')
        my_crawler = Crawler(db)
        my_crawler.retrieve_information('Python', 1)
        self.assertGreater(os.stat('data/dbfile.sqlite').st_size, 0)

    def test_retrieve_comments_score_users(self):
        db = Database.initialize_db('data/dbfile.sqlite')
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_total_user_comments_score('Python', 1)
        self.assertEquals(list, type(result))
        self.assertTrue('author' in result[0])
        self.assertTrue('score' in result[0])

    def test_retrieve_user_posts(self):
        db = Database.initialize_db('data/dbfile.sqlite')
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_user_posts('guillemnicolau', 1)
        self.assertEquals(list, type(result))
        self.assertTrue('title' in result[0])
        self.assertTrue('subreddit' in result[0])

    def test_retrieve_user_comments(self):
        db = Database.initialize_db('data/dbfile.sqlite')
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_user_comments('guillemnicolau', 1)
        self.assertEquals(list, type(result))
        self.assertTrue('comment' in result[0])
        self.assertTrue('subreddit' in result[0])

    def test_retrieve_avg_karma(self):
        db = Database.initialize_db('data/dbfile.sqlite')
        my_crawler = Crawler(db)
        result = my_crawler.retrieve_user_avg_karma('guillemnicolau', 10)
        self.assertTrue(float, type(result))