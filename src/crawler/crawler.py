import praw


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

        cursor = self.db.connection.cursor()

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS submissions(submission_title TEXT PRIMARY KEY,
                                                       external_url TEXT,
                                                       discussion_url TEXT,
                                                       submitter TEXT,
                                                       punctuation INTEGER,
                                                       creation_date TEXT,
                                                       num_comments INTEGER)
                """)

        self.db.connection.commit()

        for submission in subreddit.get_hot(limit=hot_limit):
            cursor.execute('''INSERT OR REPLACE INTO submissions(submission_title,
                                                      external_url,
                                                      discussion_url,
                                                      submitter,
                                                      punctuation,
                                                      creation_date,
                                                      num_comments)
                              VALUES(?,?,?,?,?,?,?)''', (str(submission.title),
                                                         str(submission.permalink),
                                                         str(submission.url),
                                                         str(submission.author),
                                                         int(submission.score),
                                                         str(submission.created),
                                                         int(submission.comments.__len__())))
            self.db.connection.commit()
