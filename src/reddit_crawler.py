#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import argparse
import urllib
import urllib2
import logging
import json
import re
import os
import dateutil.parser
from data_processing.data_processing import ProcessData

GET, POST = range(2)

logging.basicConfig(filename='reddit_crawler.log', level=logging.DEBUG)


def clean_screen():
    # Method called to do a 'clear', just for application visualization purposes
    print(chr(27) + "[2J")


def message_header():
    # Print method for the header of the application
    print "******************************\n* Reddit Crawler Application *\n******************************"
    print "This is an application that obtains statistics of a given subreddit or reddit user"


def message_output():
    # Print method for the input modes
    show_modes()
    print " REFRESH - Update all database data\n" + \
          " DELETE - Delete all database data\n" + \
          " HELP - Show the initial application message\n" + \
          " MODES - Show the available modes\n" + \
          " EXIT - Quit application"


def show_modes():
    # Print method for the available modes
    print "Available modes:"
    print " 1 - Retrieve or update data from subreddit and store it in Database\n" + \
          " 2 - Get Pages by Score Ranking\n" + \
          " 3 - Get Pages by Comment Ranking\n" + \
          " 4 - Get Users by Submissions Score Ranking\n" + \
          " 5 - Get Users by Submissions Quantity\n" + \
          " 6 - Get Users by Comment Score\n" + \
          " 7 - Get Posts by User\n" + \
          " 8 - Get Comments by User\n" + \
          " 9 - Get Karma Stats from User"


def check_input(input_var):
    # Method to check if the user wants to finish the application
    if input_var.lower() == 'exit':
        print "The application will now end."
        clean_screen()
        raise SystemExit
    elif input_var.lower() == 'modes':
        show_modes()
        return False
    elif input_var.lower() == 'help':
        message_output()
        return False
    elif input_var.lower() == 'delete':
        try:
            os.remove('src/rest_api/database/data/dbfile.sqlite')
            print "Database data removed"
        except Exception as e:
            print "Error trying to remove Database data:", e
        return False
    elif input_var.lower() == 'refresh':
        try:
            os.remove('src/rest_api/database/data/dbfile.sqlite')
            print "Database data removed"
        except Exception as e:
            print "Error trying to remove Database data:", e
        return True
    try:
        if int(input_var) not in range(0, 10):
            print "Please enter a valid mode."
            return False
    except:
        print "Please enter a valid mode."
        return False
    return True


def decode_date(d):
    """
    The server sent us a date in the ISO format. Convert it to a datetime
    python object.
    """
    return dateutil.parser.parse(d)


def retrieve_data(subreddit, pages):
    """
    For each page in the first n pages of a given subreddit, store its data
    in the RestAPI Database.
    """
    logging.debug('retrieve_data method called with parameters:' +
                  str(subreddit) + ", " +
                  str(pages))
    try:
        get_response("fetch_subreddit", {"chosen_subreddit": subreddit, "num_pages": pages}, method=POST)
        print "Database updated"
    except Exception as e:
        print "e:", e

_reddit_url = re.compile('.*https://www.reddit.com/r/+.*')


def get_score_ranking():
    """
    Show the top10 pages, by points
    """
    logging.debug('get_score_ranking method called')
    print "------------------ TOP PAGES RANKINGS BY SCORE ------------------"
    outside_pages = []
    comment_pages = []
    any_kind = []
    try:
        res = json.loads(get_response("get_score_ranking", {}, method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_by_score(res['result'])):
                m = _reddit_url.match(entry[2])
                if m is not None:
                    comment_pages.append((entry[0], entry[1], entry[2]))
                else:
                    outside_pages.append((entry[0], entry[1], entry[2]))
                any_kind.append((entry[0], entry[1], entry[2]))
            print "---------- Top pages rankings by score - Outside Links ----------"
            for ind, entry in enumerate(outside_pages):
                print "Top " + str(ind + 1) + " - Score: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by score - Comment Links ----------"
            for ind, entry in enumerate(comment_pages):
                print "Top " + str(ind + 1) + " - Score: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by score - Any kind of Links ----------"
            for ind, entry in enumerate(any_kind):
                print "Top " + str(ind + 1) + " - Score: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_discussion_ranking():
    """
    Show the top10 pages, by comments
    """
    logging.debug('get_discussion_ranking method called')
    print "---------- TOP PAGES RANKINGS BY COMMENTS SCORE ----------"
    outside_pages = []
    comment_pages = []
    any_kind = []
    try:
        res = json.loads(get_response("get_discussion_ranking", {}, method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_by_comments(res['result'])):
                m = _reddit_url.match(entry[2])
                if m is not None:
                    comment_pages.append((entry[0], entry[1], entry[2]))
                else:
                    outside_pages.append((entry[0], entry[1], entry[2]))
                any_kind.append((entry[0], entry[1], entry[2]))
            print "---------- Top pages rankings by comments - Outside Links ----------"
            for ind, entry in enumerate(outside_pages):
                print "Top " + str(ind + 1) + " - Comments: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by comments - Comment Links ----------"
            for ind, entry in enumerate(comment_pages):
                print "Top " + str(ind + 1) + " - Comments: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by comments - Any kind of Links ----------"
            for ind, entry in enumerate(any_kind):
                print "Top " + str(ind + 1) + " - Comments: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_top_users_by_submissions_score(subreddit):
    """
    Show the top10 users of a subreddit, by submission score
    """
    logging.debug('get_top_users_by_submissions_score method called')
    print "---------- Top Submitters ----------"
    try:
        res = json.loads(get_response("get_top_users_by_submissions_score",
                                      {"chosen_subreddit": subreddit},
                                      method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_authors_by_submission_score(res['result'])):
                print "Top " + str(ind + 1) + " - Submissions score: " + str(entry[0]) + " Author: " + str(entry[1])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_top_users_by_submissions(subreddit):
    """
    Show the top10 users of a subreddit, by number of submissions
    """
    logging.debug('get_top_users_by_submissions method called')
    print "---------- Most Active Users ----------"
    try:
        res = json.loads(get_response("get_top_users_by_submissions", {"chosen_subreddit": subreddit}, method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_authors_by_submissions(res['result'])):
                print "Top " + str(ind + 1) + " - Submissions: " + str(entry[0]) + " Author: " + str(entry[1])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_top_users_by_score(subreddit):
    """
    Show the top10 users of a subreddit, by comments score
    """
    logging.debug('get_top_users_by_score method called')
    print "---------- Top commenters ----------"
    try:
        res = json.loads(get_response("get_top_users_by_comments_score", {"chosen_subreddit": subreddit}, method=GET))
        for ind, entry in enumerate(ProcessData.sort_authors_by_score(res['result'])):
            print "Top " + str(ind + 1) + " -  Score: " + str(entry[0]) + " Author: " + str(entry[1])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_posts_by_user(chosen_username):
    """
    Show the first 10 posts for a given users
    """
    logging.debug('get_posts_by_user method called')
    print "---------- Posts by the user " + str(chosen_username) + " ----------"
    try:
        res = json.loads(get_response("get_posts_by_user", {"chosen_username": chosen_username}, method=GET))
        for ind, entry in enumerate(res['result']):
            print "Post " + str(ind + 1) + " - Title: " + str(entry['title']) + \
                  " Subreddit: " + str(entry['subreddit'])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_comments_by_user(chosen_username):
    """
    Show the top10 users, by comments score
    """
    logging.debug('get_comments_by_user method called')
    print "---------- Comments by the user " + str(chosen_username) + " ----------"
    try:
        res = json.loads(get_response("get_comments_by_user", {"chosen_username": chosen_username}, method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        for ind, entry in enumerate(res['result']):
            print "Post " + str(ind + 1) + " - Comment: " + str(entry['comment']) + \
                  " Subreddit: " + str(entry['subreddit'])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_karma_stats(chose_username):
    """
    Show the average karma of the comments for a given user
    """
    logging.debug('get_karma_stats method called')
    print "---------- Karma statistics of the user " + str(chose_username) + " ----------"
    try:
        res = json.loads(get_response("get_karma_stats", {"chosen_username": chose_username}, method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        print "Average_karma: " + str(res['result'][0]['avg_karma'])
    except Exception as e:
        print "e:", e


def get_response(fct, data, method=GET):
    """
    Performs the query to the server and returns a string containing the
    response.
    """
    assert(method in (GET, POST))
    url = 'http://%s:%s/%s' % (hostname, port, fct)
    req = ''
    if method == GET:
        req = urllib2.Request('%s?%s' % (url, urllib.urlencode(data)))
    elif method == POST:
        req = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(req)
    return response.read()


# Main method
if __name__ == "__main__":
    clean_screen()
    message_header()
    message_output()

    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-H', action="store", dest="hostname",
                        default="localhost", type=str)
    parser.add_argument('-P', action="store", dest="port",
                        default=8080, type=int)
    parser.add_argument('--specify-subreddit', action="store", dest="subreddit",
                        help="Specify the subreddit from where to fetch", default='Python')
    parser.add_argument('--specify-pages', action="store", dest="pages",
                        help="Specify the num of pages to fetch", default=100)
    parser.add_argument('--specify-user', action="store", dest="username",
                        help="Specify the name of the username to analyze", default='guillemnicolau')

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    chosen_subreddit = args.subreddit
    num_pages = int(args.pages)
    username = args.username

    while True:
        correct_input = False
        while not correct_input:
            print "***************************"
            var = raw_input("Please, enter a new mode: ")
            correct_input = check_input(var)
        if var.lower() == 'refresh' or int(var) == 1:
            retrieve_data(chosen_subreddit, num_pages)
        elif int(var) == 2:
            get_score_ranking()
        elif int(var) == 3:
            get_discussion_ranking()
        elif int(var) == 4:
            get_top_users_by_submissions_score(chosen_subreddit)
        elif int(var) == 5:
            get_top_users_by_submissions(chosen_subreddit)
        elif int(var) == 6:
            get_top_users_by_score(chosen_subreddit)
        elif int(var) == 7:
            get_posts_by_user(username)
        elif int(var) == 8:
            get_comments_by_user(username)
        elif int(var) == 9:
            get_karma_stats(username)
