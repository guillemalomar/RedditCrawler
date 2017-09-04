import praw
import unidecode
import sqlite3
import errno
import os.path


class Database:

    def __init__(self, db_file_name):
        self.connection = Database.initialize_db(db_file_name)

    @staticmethod
    def initialize_db(db_file_name):
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
        db_file = open(db_file_name, 'w')
        db_file.close()
        return sqlite3.connect(db_file_name, check_same_thread=False)


class Crawler:
    def __init__(self, db):
        self.db = db
        self.reddit = praw.Reddit('bot1')

    def retrieve_information(self, subreddit, hot_limit):
        # This method the first n pages (defined by 'hot_limit' parameter) from a
        # given subreddit (defined by 'subreddit' parameter) and stores their
        # important information in the crawler database.
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

    def retrieve_comments(self, chosen_subreddit):
        # This method the first n pages (defined by 'hot_limit' parameter) from a
        # given subreddit (defined by 'subreddit' parameter) and stores their
        # important information in the crawler database.
        try:
            subreddit = self.reddit.get_subreddit(chosen_subreddit)
        except Exception as e:
            print "Error when trying to obtain subreddit information:", e
            raise RuntimeError
        comments = {}
        for submission in subreddit.get_hot(limit=1):
            for comment in submission.comments:
                try:
                    comments[str(comment.author.name)] = comments.get(str(comment.author.name), 0) + comment.score
                except Exception as e:
                    print "Error:", e
        to_return = []
        for author, score in comments.iteritems():
            to_return.append({'author': author, 'score': score})
        return to_return

    def retrieve_user_posts(self, chosen_username):
        user = self.reddit.get_redditor(chosen_username)
        gen = user.get_submitted(limit=10)
        user_comments = []
        for thing in gen:
            user_comments.append({'title': thing.title, 'subreddit': thing.subreddit.title})
        return user_comments

    def retrieve_user_comments(self, chosen_username):
        user = self.reddit.get_redditor(chosen_username)
        gen = user.get_comments(limit=10)
        user_comments = []
        for thing in gen:
            user_comments.append({'comment': thing.body, 'subreddit': thing.subreddit.title})
        return user_comments

    def retrieve_user_avg_karma(self, chosen_username):
        user = self.reddit.get_redditor(chosen_username)
        gen = user.get_comments(limit=10)
        user_comments = []
        user_karma = 0
        for ind, thing in enumerate(gen):
            user_karma += thing.score
        user_comments.append({'user': chosen_username, 'avg_karma': float(user_karma)/ind+1})
        return user_comments

my_db = Database.initialize_db('test/testdbfile.sqlite')
my_crawler = Crawler(my_db)
my_crawler.retrieve_information('Python', 100)
# my_crawler.retrieve_comments('Python')
# my_crawler.retrieve_user_posts('guillemnicolau')
# my_crawler.retrieve_user_comments('guillemnicolau')
# my_crawler.retrieve_user_avg_karma('guillemnicolau')
